import boto3
import csv
import io
import logging
from datetime import datetime
from botocore.exceptions import ClientError

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
secrets_client = boto3.client('secretsmanager')


def get_secret(secret_name):
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in response:
            return response['SecretString']
        return None
    except ClientError as e:
        logging.error(e)
        return None


def lambda_handler(event, context):
    try:
        # Fetch secrets
        secret = get_secret("YourSecretName")
        if not secret:
            raise Exception("Failed to fetch secret")

        # Connect to DynamoDB and fetch data
        table = dynamodb.Table(secret['TableName'])
        items = table.scan()['Items']

        # Convert the data to CSV format
        output = io.StringIO()
        writer = csv.writer(output)
        # Assuming all items have same keys
        headers = items[0].keys()
        writer.writerow(headers)
        for item in items:
            writer.writerow(item.values())

        # Upload to S3 in the format year/month/date/filename.csv
        today = datetime.today()
        folder = today.strftime('%Y/%m/%d')
        file_name = "your_filename.csv"
        s3_path = f"{folder}/{file_name}"

        s3.put_object(Bucket=secret['BucketName'],
                      Key=s3_path, Body=output.getvalue())
        logger.info(f"File uploaded to S3: {s3_path}")

    except Exception as e:
        logger.error(f"Error: {e}")
        # You can further customize the error message to provide more detailed feedback
        return {
            'statusCode': 500,
            'body': 'An error occurred. Check CloudWatch logs for more details.'
        }

    return {
        'statusCode': 200,
        'body': 'CSV file successfully generated and uploaded to S3'
    }


# This is how you are going to do the secrets
# {
#    "TableName": "YourDynamoDBTableName",
#    "BucketName": "YourS3BucketName"
# }
