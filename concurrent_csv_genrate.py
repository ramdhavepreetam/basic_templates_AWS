import psycopg2
import csv
import boto3
from io import StringIO
from datetime import datetime
import json
import logging
from concurrent.futures import ThreadPoolExecutor

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

def fetch_data_from_db(cur, query):
    try:
        cur.execute(query)
        return cur.fetchall()
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        raise

def create_s3_folder(all_data, dealerID, bucket_name):
    try:
        output = StringIO()
        csv_writer = csv.writer(output)
        csv_writer.writerows(all_data)

        # Construct the folder structure: dealerID/year/month/day/ITEM.csv
        current_date = datetime.now()
        folder_structure = f"{dealerID}/{current_date.strftime('%Y/%m/%d')}"
        s3_key = f"{folder_structure}/ITEM.csv"
        
        output.seek(0)
        
        resource = boto3.resource('s3')
        resource.Object(bucket_name, s3_key).put(Body=output.getvalue())
        logging.info(f"Successfully uploaded to {s3_key}")
    except Exception as e:
        logging.error(f"Error creating S3 folder: {e}")
        raise

def process_dealer_code(item, cur, bucket_name):
    try:
        query = f"SELECT * FROM PPDGLOBAL.\"DCPP0113C\" DD WHERE DD.\"ITMID\" IN ((SELECT DC.\"ITMID\" FROM PPDGLOBAL.\"DCPP0115\" DC WHERE  DC.\"CSTNO\" = '{item[0].replace(' ', '')}'))"
        secondary_data = fetch_data_from_db(cur, query)
        
        folder_value = item[0].replace(' ', '')
        create_s3_folder(secondary_data, folder_value, bucket_name)
    except Exception as e:
        logging.error(f"Error processing dealer code {item[0]}: {e}")
        raise 

def lambda_handler(event, context):
    try:
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
        
        initial_data = fetch_data_from_db(cur, "SELECT distinct \"DEALER_CODE\" FROM ppdglobal.\"DEALER_MASTER\"")
        
        # Use ThreadPoolExecutor to process dealer codes in parallel
        with ThreadPoolExecutor() as executor:
            # Here, process_dealer_code will be called with each item from initial_data
            executor.map(lambda item: process_dealer_code(item, cur, secrets['BucketName']), initial_data)
        
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
