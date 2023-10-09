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





Certainly! Here's the complete Lambda function with the modifications:

```python
import json
import requests
import boto3

def get_secret():
    secret_name = "YOUR_SECRET_NAME"
    region_name = "YOUR_AWS_REGION"
    
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        raise e  # Handle this according to your logging or error handling preference

    if 'SecretString' in get_secret_value_response:
        secret = json.loads(get_secret_value_response['SecretString'])
        return secret
    else:
        raise Exception("Failed to retrieve secret values.")

def get_values_from_api(ORDNO, CSTNO, CSTSFX, ITMID):
    # API endpoint
    url = "http://ppdtest:10010/web/services/RetrieveOrderInfo"
    
    # Retrieve username and password from Secrets Manager
    secrets = get_secret()
    username = secrets['username']
    password = secrets['password']
    
    # Encode to base64 for basic authentication
    auth_token = f"{username}:{password}"
    
    headers = {
        "Authorization": f"Basic {auth_token.encode().decode('base64')}"
    }
    
    # API payload
    payload = {
        "ORDNO": ORDNO,
        "CSTNO": CSTNO,
        "CSTSFX": CSTSFX,
        "ITMID": ITMID
    }
    
    # Making the API request
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Extract data from API response
        response_data = response.json()
        if response_data.get("ErrorResponse") and response_data["ErrorResponse"].get("IsSuccess") == "true":
            return response_data.get("OutData", {}).get("OutDataS", [])
        else:
            return "ERROR"
    except requests.exceptions.RequestException as e:
        raise e  # Handle this according to your logging or error handling preference

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])  # Parsing the body to extract parameters
        ORDNO = body['ORDNO']
        CSTNO = body['CSTNO']
        CSTSFX = body['CSTSFX']
        ITMID = body['ITMID']

        result = get_values_from_api(ORDNO, CSTNO, CSTSFX, ITMID)
        
        if result == 'ERROR':
            return {
                "statusCode": 500,
                "body": "Server Error"
            }
        else:
            return {
                "statusCode": 200,
                "body": json.dumps(result)
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Server Error: {str(e)}"
        }
```

In this code:

1. The `get_secret()` function retrieves credentials from the AWS Secrets Manager.
2. The `get_values_from_api()` function calls the specified API with basic authentication using the credentials retrieved.
3. The `lambda_handler()` function is the entry point for the Lambda execution. It extracts the parameters (`ORDNO`, `CSTNO`, `CSTSFX`, `ITMID`) from the body of the request and then calls the `get_values_from_api()` function.

Make sure to replace the placeholders `YOUR_SECRET_NAME` and `YOUR_AWS_REGION` with appropriate values for your setup. Ensure that the Lambda has the necessary IAM permissions and that the `boto3` and `requests` libraries are included in the deployment package.

import http.client
import json
import boto3

def get_secret():
    # ... (no changes here, same as before)

def get_values_from_api(ORDNO, CSTNO, CSTSFX, ITMID):
    # API endpoint details
    host = "ppdtest"
    port = 10010
    path = "/web/services/RetrieveOrderInfo"
    
    # Retrieve username and password from Secrets Manager
    secrets = get_secret()
    username = secrets['username']
    password = secrets['password']
    
    # Set up basic authentication header
    auth_token = f"{username}:{password}"
    headers = {
        "Authorization": f"Basic {auth_token.encode().decode('base64')}",
        "Content-Type": "application/json"
    }
    
    # API payload
    payload = {
        "ORDNO": ORDNO,
        "CSTNO": CSTNO,
        "CSTSFX": CSTSFX,
        "ITMID": ITMID
    }

    # Making the API request using http.client
    conn = http.client.HTTPConnection(host, port)
    conn.request("POST", path, body=json.dumps(payload), headers=headers)

    response = conn.getresponse()
    data = response.read().decode('utf-8')
    conn.close()

    if response.status == 200:
        response_data = json.loads(data)
        if response_data.get("ErrorResponse") and response_data["ErrorResponse"].get("IsSuccess") == "true":
            return response_data.get("OutData", {}).get("OutDataS", [])
        else:
            return "ERROR"
    else:
        raise Exception(f"API request failed with status {response.status} and response: {data}")

def lambda_handler(event, context):
    # ... (no changes here, same as before)



        [ERROR]	2023-10-05T17:26:38.277Z	0affed40-2cab-49cf-9951-7c56e04459b7	Unexpected error: list_all_objects() missing 1 required positional argument: 'prefix'
