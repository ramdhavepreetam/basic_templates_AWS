import psycopg2
import boto3
import json
import logging
from io import StringIO
import csv

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
    query = f"""SELECT * FROM PPDGLOBAL."DCPP0113C" DD WHERE DD."ITMID" IN (
                   SELECT DC."ITMID" FROM PPDGLOBAL."DCPP0115" DC WHERE DC."CSTNO" = '{dealer_id}'
               )"""
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
    folder_structure = f"{dealerID}/{current_date.strftime('%Y/%m/%d')}"
    s3_key = f"{folder_structure}/ITEM.csv"
    
    output.seek(0)
    resource = boto3.resource('s3')
    resource.Object(bucket_name, s3_key).put(Body=output.getvalue())
    logging.info(f"Successfully uploaded data for dealer ID {dealerID} to {s3_key}")

def lambda_handler(event, context):
    try:
        secrets = get_secrets('your_secret_id')  # Replace 'your_secret_id' with the appropriate secret ID
        
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
            dealer_id = payload['dealer_code']

            data = fetch_data_from_db(cur, dealer_id)
            save_to_s3(data, dealer_id, secrets['BucketName'])

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


'''
{
  "Records": [
    {
      "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
      "receiptHandle": "MessageReceiptHandle",
      "body": "{\"dealer_code\": \"K035\", \"filetype\": \"daily\"}",
      "attributes": {
        "ApproximateReceiveCount": "1",
        "SentTimestamp": "1523232000000",
        "SenderId": "123456789012",
        "ApproximateFirstReceiveTimestamp": "1523232000001"
      },
      "messageAttributes": {},
      "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",  // This is just a sample MD5 hash. In a real event, it would be computed based on the body's contents.
      "eventSource": "aws:sqs",
      "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
      "awsRegion": "us-east-1"
    }
  ]
}

'''
