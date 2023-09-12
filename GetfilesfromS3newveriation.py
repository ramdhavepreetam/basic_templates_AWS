import boto3
import logging
import json
from botocore.exceptions import ClientError
from urllib.parse import unquote_plus

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the clients outside the handler
s3_client = boto3.client('s3')
secrets_manager = boto3.client('secretsmanager')


def list_all_objects(bucket_name, prefix):
    """Retrieve all objects under a specific prefix in an S3 bucket"""
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    all_objects = response.get('Contents', [])
    
    while response.get('IsTruncated', False):
        continuation_token = response.get('NextContinuationToken')
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, ContinuationToken=continuation_token)
        all_objects.extend(response.get('Contents', []))
        
    return [obj['Key'] for obj in all_objects]


def lambda_handler(event, context):
    try:
        s3_bucket = event.get('s3Bucket', None)
        s3_prefix = unquote_plus(event.get('objectName', ''), encoding='utf-8')  # Prefix instead of object name
        date = event.get('Date', None)
        
        # Retrieve expiration time from Secrets Manager
        secret_value_response = secrets_manager.get_secret_value(SecretId='your_secret_id')
        secret = json.loads(secret_value_response['SecretString'])
        expiration_time = int(secret['ExpiresIn'])  # Assuming the key in secret is "ExpiresIn"

        all_objects = list_all_objects(s3_bucket, s3_prefix)
        
        urls = [
            {
                "Fileurl": s3_client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': s3_bucket,
                        'Key': obj_key,
                    },
                    ExpiresIn=expiration_time
                )
            }
            for obj_key in all_objects
        ]

        return {
            'Urls': urls
        }

    except ClientError as e:
        logger.error(f"ClientError: {e}")
        return {
            'error': str(e)
        }

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            'error': 'An unexpected error occurred.'
        }
