import psycopg2
import boto3
import json
import logging
from io import StringIO
import csv
from datetime import datetime
logging.basicConfig(level=logging.INFO)


def get_secrets(secret_id):
    try:
        secrets_client = boto3.client('secretsmanager')
        response = secrets_client.get_secret_value(SecretId=secret_id)
        secrets = json.loads(response['SecretString'])
        return secrets
    except Exception as e:
        logging.error(f"Error fetching secrets: {e}")
        raise


def connect_to_db(db_params):
    try:
        conn = psycopg2.connect(**db_params)
        return conn
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        raise


def fetch_data_from_db(cur, dealer_id):
    query = f"""
        WITH PRICING_DATA AS (
        SELECT DISTINCT
        a."PRICEID",b."CSTNO",b."CSTSFX",a."ITMID",a."EFFDATE",a."PDCFRZ",a."DSPFRZ",
        a."CHANNEL",a."CLIST",a."RESALE", a."STDDLRNET",a."BESTCODE",a."QTYBREAK",a."QTYDISC",
        a."QTYPRICE",a."QTYFNL",a."QTBRKEND",a."PROMO",a."PROMOPCT",a."SANBR",a."PHASE",
        a."SALINE",a."BASEQTY",a."SABSTNET",a."SAEFFDATE",a."SAEXPDATE",a."FNLNET",
        c."GLFINENT",d."CORFLG",d."CORPRC",d."CORGRP",d."CORCLS",e."GRPCDE"
               FROM (
        SELECT * FROM ppdglobal."DCPP0113U"
        UNION ALL
        SELECT * FROM ppdglobal."DCPP0113C"
        UNION ALL
        SELECT * FROM ppdglobal."DCPP0113M"
        UNION ALL
        SELECT * FROM ppdglobal."DCPP0113P"
        ) AS a
        JOIN ppdglobal."DCPP0115" AS b ON a."PRICEID" = b."PRICEID"
        LEFT JOIN ppdglobal."DOPCMST0" AS c ON c."CSTNO" = b."CSTNO" AND c."CSTSFX" = b."CSTSFX"
        LEFT JOIN ppdglobal."DCPP0111" AS d ON a."ITMID" = d."ITMID" AND c."GLFINENT" = d."GLFINENT"
        LEFT JOIN ppdglobal."DCPP0124" AS e ON a."ITMID" = e."ITMID"
        )
        SELECT *
        FROM PRICING_DATA y
        WHERE EXISTS (
        SELECT 1
        FROM (
        SELECT "LOC", "P_DBS" FROM PPDGLOBAL."LOC_PB"
        UNION ALL
        SELECT "LOC", "P_DBS" FROM PPDGLOBAL."LOC_KW"
        ) AS LOCATION_DATA
        WHERE LOCATION_DATA."LOC" = y."CSTNO"
        AND LOCATION_DATA."P_DBS" = '{dealer_id.replace(' ', '')}')
       
        """
    try:
        cur.execute(query)
        return cur.fetchall()
    except Exception as e:
        logging.error(f"Error executing query for dealer ID {dealer_id}: {e}")
        raise


def save_to_s3(all_data, dealerID, bucket_name):
    output = StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerows(all_data)

    current_date = datetime.now()
    folder_structure = f"Custom/Dbs/Daily/{dealerID}/{current_date.strftime('%Y/%m')}"
    s3_key = f"{folder_structure}/PRICE.csv"

    output.seek(0)
    resource = boto3.resource('s3')
    resource.Object(bucket_name, s3_key).put(Body=output.getvalue())
    print(f"Successfully uploaded data for dealer ID {dealerID} to {s3_key}")
    logging.info(
        f"Successfully uploaded data for dealer ID {dealerID} to {s3_key}")

def save_to_s3_to_append(all_data, dealerID, bucket_name):
    
    current_date = datetime.now()
    folder_structure = f"Custom/Dbs/Daily/{dealerID}/{current_date.strftime('%Y/%m')}"
    s3_key = f"{folder_structure}/PRICE.csv"
    client = boto3.client('s3')
    try:
        current_data = client.get_object(Bucket=bucket_name, Key=s3_key)
        data=current_data['Body'].read()
        output = StringIO()
        csv_writer = csv.writer(output)
        csv_writer.writerows(all_data)
        print("data:",data)
        new_data=output.getvalue().encode('utf-8')
        print("new_data:",new_data)
        client.put_object(Body=data+new_data,Bucket=bucket_name,Key=s3_key)
    
        print("successfully")
        
    except Exception as e:
        logging.error(f"Error in the Lambda handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"{s3_key} is not available")
        }
    

def lambda_handler(event, context):
    try:
        print(event)
        # Replace 'your_secret_id' with the appropriate secret ID
        secrets = get_secrets('ppd-dev-pricefile-modernization')

        DB_PARAMS = {
            'dbname': secrets['dbname'],
            'user': secrets['user'],
            'password': secrets['password'],
            'host': secrets['host'],
            'port': secrets['port']
        }

        conn = connect_to_db(DB_PARAMS)
        cur = conn.cursor()

        # Get dealer_id from the SQS message
        for record in event['Records']:
            payload = json.loads(record['body'])
            dealer_id = payload['dbs_code']
            
            #Current_date=datetime.today().day

            #if Current_date==1:
               # return
            
            #elif Current_date==2:
            data = fetch_data_from_db(cur, dealer_id)
            save_to_s3(data, dealer_id, secrets['BucketName'])
            #else:
                #data = fetch_data_from_db(cur, dealer_id)
                #save_to_s3_to_append(data, dealer_id, secrets['BucketName'])


        cur.close()
        conn.close()

        return {
            'statusCode': 200,
            'body': json.dumps('Data successfully processed and uploaded to S3!')
        }

    except Exception as e:
        logging.error(f"Error in the Lambda handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('An error occurred. Check logs for details.')
        }
