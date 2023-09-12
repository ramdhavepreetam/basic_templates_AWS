import boto3
import json
import logging
from urllib.parse import unquote_plus

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_secret_value(secret_name):
    """
    Fetch secret value from AWS Secrets Manager.
    """
    secrets_client = boto3.client('secretsmanager')
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in response:
            secret = response['SecretString']
            return json.loads(secret)
        else:
            raise ValueError("SecretString not found in the secret response")
    except Exception as e:
        logger.error(f"Unable to retrieve secret: {str(e)}")
        raise RuntimeError(f"Unable to retrieve secret: {str(e)}")

def lambda_handler(event, context):
    logger.info("Lambda execution started")
    logger.info(f"Received event: {json.dumps(event)}")
    
    #s3_bucket = event['s3bucket']
    s3_bucket = event.get('s3bucket',None)
 
    date = event['date']

    # Retrieve ExpiresIn from Secrets Manager
    secret_name = "SECREATE_NAME_****"
    try:
        logger.info("i am in try block")
        secrets = get_secret_value(secret_name)

        expires_in = int(secrets['ExpiresIn'])
        logger.error(f"Got Expires in the secreates : {str(expires_in)}")
    except Exception as e:
        logger.error(f"Failed to fetch ExpiresIn value from Secrets Manager: {str(e)}")
        error_response = {
            "error": "Error fetching ExpiresIn value from Secrets Manager."
        }
        return json.dumps(error_response)

    s3 = boto3.client('s3')
    urls = []

    try:
        logger.info("i am in try of the gets3 bucket objects")
        objects = s3.list_objects_v2(Bucket=s3_bucket,)
        
        logger.info(f"Received Objects are : {json.dumps(objects)}")        
        if 'Contents' not in objects:
            error_response = {
                "error": "No files found in the provided location."
            }
            logger.warning("No files found in the provided S3 location")
            return json.dumps(error_response)

        for obj in objects['Contents']:
            key = unquote_plus(obj['Key'], encoding='utf-8')
            url = s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': s3_bucket, 'Key': key},
                ExpiresIn=expires_in
            )
            urls.append({"Fileurl": url})

        response = {
            "Urls": urls
        }
        return json.dumps(response)

    except s3.exceptions.NoSuchBucket:
        error_message = "The specified bucket does not exist."
        logger.error(error_message)
        error_response = {
            "error": error_message
        }
        return json.dumps(error_response)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logger.error(error_message)
        error_response = {
            "error": error_message
        }
        return json.dumps(error_response)
