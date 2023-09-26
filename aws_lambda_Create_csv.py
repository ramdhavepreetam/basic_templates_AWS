import psycopg2
import csv
import boto3
from io import StringIO
from datetime import datetime
import json
import logging
# Fetch the secret from AWS Secrets Manager
secrets_client = boto3.client('secretsmanager')
response = secrets_client.get_secret_value(
    SecretId='ppd-dev-pricefile-modernization')
secrets = json.loads(response['SecretString'])

DB_PARAMS = {
    'dbname': secrets['dbname'],
    'user': secrets['user'],
    'password': secrets['password'],
    'host': secrets['host'],
    'port': secrets['port']
}

# Create a CSV in-memory


def create_s3_folder(all_data, dealerID):

    output = StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerows(all_data)
    # Upload the CSV to Amazon S3
    s3_client = boto3.client('s3')
    s3_bucket = secrets['BucketName']
    folder_name = "{}_{}".format(dealerID, datetime.now().strftime('%Y_%m_%d'))
    s3_key = f"{folder_name}/ITEM.csv"
    se_key_utfencoded = s3_key.encode('utf-8')
    output.seek(0)
    logging.info(output.getvalue())
    # s3_client.upload_fileobj(output, s3_bucket, s3_key)
    resource = boto3.resource('s3')
    resource.Object(s3_bucket, s3_key).put(Body=output.getvalue())


# Connect to PostgreSQL
conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

# Execute initial SQL query
initial_query = "SELECT distinct \"DEALER_CODE\" FROM ppdglobal.\"DEALER_MASTER\""
cur.execute(initial_query)
initial_data = cur.fetchall()

# Loop through the first column and execute secondary queries
all_data = []
for item in initial_data:
    secondary_query = f"SELECT * FROM PPDGLOBAL.\"DCPP0113C\" DD WHERE DD.\"ITMID\" IN ((SELECT DC.\"ITMID\" FROM PPDGLOBAL.\"DCPP0115\" DC WHERE  DC.\"CSTNO\" = '{item[0].replace(' ', '')}'))"
    cur.execute(secondary_query)
    secondary_data = cur.fetchall()
    all_data.extend(secondary_data)
    folder_value = item[0].replace(' ', '')
    create_s3_folder(secondary_data, folder_value)


# Close database connection
cur.close()
conn.close()
