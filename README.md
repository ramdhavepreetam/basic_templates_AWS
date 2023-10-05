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



https://s3.us-west-2.amazonaws.com/ppd.dev.paricefile.bucket/Custom/Monthly/CDK/2023/10/ITEM.csv?AWSAccessKeyId=ASIAT7LJPKWNZPPQC77C&Signature=vOFSU4Z2r4cld9UDj6s%2FOl9QvR4%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEFsaCXVzLXdlc3QtMiJHMEUCIBEk0QVHIv4b6spV4EwjwzZbcurTlq8qH5OO7eZBhUU9AiEAoA%2FSn2Rv4PX8HeJdyi5zQUjrPKCyDGUkQ8xVItxnr9sqjwMIZBADGgwyNzM0ODg1MDAxMjMiDHxS8CF9SOhNBevpZyrsAnfM3b%2B%2BwQSyJNdQKYPAF%2BXbBUJ3XxJYN3bAhqLZd6n7OOcPASt15c9sPiBsJgQq9EQEEMmEuWj4SAOoF2ypx0EJTWXjl8J4SvXP6zipyaJW7yHG0LBHrXf%2BXvyO6Bp9T85h8yneXsgUDXnMGQyenyu7RxbJBTtZig5G4bIUvgf%2FoXOrkHAT74lZmlzTUoIPwUUPBT2sjxQwZyvP%2BwLp4na3TrjUjFq%2FOal8Xho3ztU0PACvx2ftvPtnfhTQq42euaNytgY0G46v%2FT4bSHfJtpaO1k6LxsvrckWtBB%2BvGuDFEffzO6HZfOwnendlIVGJwi%2Bb86ZCeXnQfd04QvQW1ElisORW5lL57cqEjSgmCXDjJkUeOqc7933t6xk62XbE84bC2pWmlmqe4FGC4wBAnqYos0bEYs02hPhu740mxXOYTKU3jv3LY3ERp4ljMIRpjUBnJXdK0GtOFspnqlDXWU3KOC0YczOoHNiAO88wm4%2F8qAY6nQErJLzQu%2BncwMtMDwapL4nM2o0mDx7wzH4Awqs1F7AKQDCrXf7UKG6FuZv3Fr8zh3O1%2BAHzZGgdk3UT%2Fv6QU2JKSsyZ5%2B2kuU4oj8danWK%2F9%2BYJsTKU96fZeebF3OhiTlqW8i24DTO5fg0CRwer0qNR%2Fjxt%2F7bTd4cm7BVoUe8Mcu1W2m31iVA%2FTrXR8oQH3Ulefj0SXkt8e1ke2IID&Expires=1696535980"


[INFO]	2023-10-05T20:18:12.532Z	201ec249-0edf-4521-bb14-f7a59c0d3a46	{'resource': '/pricefiles/getfiles', 'path': '/pricefiles/getfiles', 'httpMethod': 'POST', 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/json', 'Host': 'iiptjvxujl.execute-api.us-west-2.amazonaws.com', 'Postman-Token': '69284672-b439-48cd-9728-485d87786760', 'User-Agent': 'PostmanRuntime/7.26.8', 'X-Amzn-Trace-Id': 'Root=1-651f1a03-5951144573752cdd24d33767', 'x-api-key': 'QwIlV9pCsm1N0div5PuYjayI2AlxgvND1U8zfY8T', 'X-Forwarded-For': '160.69.1.132', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate, br'], 'Content-Type': ['application/json'], 'Host': ['iiptjvxujl.execute-api.us-west-2.amazonaws.com'], 'Postman-Token': ['69284672-b439-48cd-9728-485d87786760'], 'User-Agent': ['PostmanRuntime/7.26.8'], 'X-Amzn-Trace-Id': ['Root=1-651f1a03-5951144573752cdd24d33767'], 'x-api-key': ['QwIlV9pCsm1N0div5PuYjayI2AlxgvND1U8zfY8T'], 'X-Forwarded-For': ['160.69.1.132'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'liwp0p', 'resourcePath': '/pricefiles/getfiles', 'httpMethod': 'POST', 'extendedRequestId': 'MWEAnGN5PHcFcqw=', 'requestTime': '05/Oct/2023:20:18:11 +0000', 'path': '/Dev/pricefiles/getfiles', 'accountId': '273488500123', 'protocol': 'HTTP/1.1', 'stage': 'Dev', 'domainPrefix': 'iiptjvxujl', 'requestTimeEpoch': 1696537091632, 'requestId': '470dcaad-f243-4597-9c26-9af14e3471cf', 'identity': {'cognitoIdentityPoolId': None, 'cognitoIdentityId': None, 'apiKey': 'QwIlV9pCsm1N0div5PuYjayI2AlxgvND1U8zfY8T', 'principalOrgId': None, 'cognitoAuthenticationType': None, 'userArn': None, 'apiKeyId': 'crz1jxldma', 'userAgent': 'PostmanRuntime/7.26.8', 'accountId': None, 'caller': None, 'sourceIp': '160.69.1.132', 'accessKey': None, 'cognitoAuthenticationProvider': None, 'user': None}, 'domainName': 'iiptjvxujl.execute-api.us-west-2.amazonaws.com', 'apiId': 'iiptjvxujl'}, 'body': '{\n    "s3Bucket" : "ppd.dev.paricefile.bucket",\n    "Prefix" :"Custom/Monthly/CDK/"\n}', 'isBase64Encoded': False}






        [ERROR]	2023-10-05T17:26:38.277Z	0affed40-2cab-49cf-9951-7c56e04459b7	Unexpected error: list_all_objects() missing 1 required positional argument: 'prefix'
