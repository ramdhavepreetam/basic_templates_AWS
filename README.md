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




import json
import time

def lambda_handler(event, context):
    # Sample data; replace with your actual API call and data processing
    vendor_name = "VendorName"
    start_time = time.time()
    
    # Your API call to the vendor goes here
    # ...

    duration = (time.time() - start_time) * 1000  # Calculate time in milliseconds
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "vendor": vendor_name,
        "requestDuration": duration,
        "logIdentifier": "VendorAPIRequest"
    }
    print(json.dumps(log_entry))


{
  "timestamp": "2023-10-12T10:00:00Z",
  "vendor": "VendorName",
  "requestDuration": 1234,  // time in milliseconds
  "logIdentifier": "VendorAPIRequest",
  "additionalInfo": "AnyOtherRelevantInfo"
}


fields @timestamp, vendor, avg(requestDuration)
| filter logIdentifier = "VendorAPIRequest"
| stats avg(requestDuration) by vendor


No aggregation function expression allowed: fields@timestamp,vendor,avg(requestDuration) ([73,119]) (Service: AWSLogs; Status Code: 400; Error Code: MalformedQueryException; Request ID: 24621266-8925-44c7-a30e-49e63788605c; Proxy: null)



