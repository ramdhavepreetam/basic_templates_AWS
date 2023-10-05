# basic_templates_AWS


[ERROR]	2023-09-12T18:47:41.651Z	4019b174-a5dd-4536-965c-fcacae31086f	Unable to retrieve secret: An error occurred (AccessDeniedException) when calling the GetSecretValue operation: User: arn:aws:sts::273488500123:assumed-role/ppdusrdevpricefileextrac/ppd-dev-get-pricefilesdetails is not authorized to perform: secretsmanager:GetSecretValue on resource: ppd-dev-pricefile-modernization because no identity-based policy allows the secretsmanager:GetSecretValue action

An error occurred: expected string or bytes-like object

Invalid bucket name "ppd.dev.paricefile.bucket/Custom/DSI": Bucket name must match the regex "^[a-zA-Z0-9.\-_]{1,255}$" or be an ARN matching the regex "^arn:(aws).*:(s3|s3-object-lambda):[a-z\-0-9]*:[0-9]{12}:accesspoint[/:][a-zA-Z0-9\-.]{1,63}$|^arn:(aws).*:s3-outposts:[a-z\-0-9]+:[0-9]{12}:outpost[/:][a-zA-Z0-9\-]{1,63}[/:]accesspoint[/:][a-zA-Z0-9\-]{1,63}$"

import json

def lambda_handler(event, context):
    # ... your code ...

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({"message": "Hello World"})
    }







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
        s3_prefix = unquote_plus(event.get('Prefix', ''), encoding='utf-8')  # Prefix instead of object name
        date = event.get('Date', None)
        
        # Retrieve expiration time from Secrets Manager
        secret_value_response = secrets_manager.get_secret_value(SecretId='ppd-dev-pricefile-modernization')
        secret = json.loads(secret_value_response['SecretString'])
        expiration_time = int(secret['ExpiresIn'])  # Assuming the key in secret is "ExpiresIn"
        logger.info('this is path ' + s3_prefix)
        all_objects = list_all_objects(s3_bucket, )
        refine_list = [item for item in all_objects if '.csv' in item]
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
            for obj_key in refine_list
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


https://s3.us-west-2.amazonaws.com/ppd.dev.paricefile.bucket/Custom/Monthly/CDK/2023/10/ITEM.csv?AWSAccessKeyId=ASIAT7LJPKWN2ZIFVSHC&Signature=BlPfCsTGlmuyiwekLSJn2QuMkvo%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEFoaCXVzLXdlc3QtMiJIMEYCIQDCcoD0e6hWSjBchUIdnDx%2FsNJVZMjN%2BMAtZKhrbmFfXQIhAPQS8sScI%2BltYvn8wyC3yNtugQrUN9iZpAFmVu8A06EAKo8DCGMQAxoMMjczNDg4NTAwMTIzIgwDqLAogLZ9IGkzVlYq7AL0vKbIaRVUKNe2KObPBRDLyCrcex6qIuB7i1eA9G5uvpxDSKwHVAMUYi4RGKtjHo1Gz%2FROiJ8KxBK4PgWc3ZrWkvZ0IL1g525qQyZ1t1szKpwasgb2BxepCJq96E9ZK0v9c1vyEfEktzZUhOGxvkL1RwVQ5VBHkHKqM1vEJ7mekr1VCWbIwLIPlKr1z5SJJdRaLehk3lQV0yWQJtRI5lKg41sLuvE04sFmfdNXgq5wUGGFCeKHru0mnilJJH6hIQWJYRGZ51z6KUXKVEJfP3iXRoYcZP2hOUQuD8lQKLGEWtrWZs%2F6U3WC04kbvfSNB%2BBHAQuzYxnJIclJSXfObKwnhWtWlTfi0Ass9fFUNjlYs8tJQ8LCoWkBAcjAaLSg%2BHwnDGuzZgHSXjcsO7eWoWpnjZyAUBmOQZkv3T2GbFYa0LS%2FC3WjNTBHwkjJZ1E3nnExOk8IE8Rvy9vYeYZYcjc6a2E6yuiYTqBHM1a8MPfs%2B6gGOpwBwNpGhcexA6C5Fhql%2FVVjiy5oyioj1UIexVO5NpNCX%2Fdq3bnG1VIQApb%2F7ApuX3Uh1niBqITkUN6dwM%2BxLQzY6NNLy9OXUuhZf1JYxg%2FtWbnEVsYx6udv5opBt8pNRGvj%2BpVfxPRsAcPjzqK0dAtNECagBC4Wc9FZSJCHG5Q7g5W3U%2BLEXW4Saz5S4n%2Bm65bnrXvlW6GS%2FX30KhFr&Expires=1696531592





        [ERROR]	2023-10-05T17:26:38.277Z	0affed40-2cab-49cf-9951-7c56e04459b7	Unexpected error: list_all_objects() missing 1 required positional argument: 'prefix'
