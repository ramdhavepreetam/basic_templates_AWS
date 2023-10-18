import json
import http.client
import boto3

def get_secret():
    secret_name = "ppd-dev-order-salseforce-api"
    region_name = "us-west-2"
    
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
    # API endpoint details
    host = "ppdtest.na.paccar.com"
    port = 10010
    path = "/web/services/RetrieveOrderInfo"
    
    # Retrieve username and password from Secrets Manager
    secrets = get_secret()
    Authorization = secrets['Authorization']
    # API payload
    payload = {
        "ORDNO": ORDNO,
        "CSTNO": CSTNO,
        "CSTSFX": CSTSFX,
        "ITMID": ITMID
    }
    # Making the API request using http.client
    conn = http.client.HTTPConnection(host, port)
    print('-----------------------------Payload Starts ----------------------------------')
    print(payload)
    print('-----------------------------Payload end -------------------------------------')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': secrets['Authorization']
    }
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
    try:
        print(json.dumps(event))
        if 'body' not in event:
            return {
                "statusCode" : 400,
                "body:" : "request body is missing"
            }
        
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




-----------------------------------------------------------------------



import json
import http.client
import boto3

def get_secret():
    secret_name = "ppd-dev-order-salseforce-api"
    region_name = "us-west-2"

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
    # API endpoint details
    host = "ppdtest.na.paccar.com"
    port = 10010
    path = f"/web/services/RetrieveOrderInfo?ORDNO={ORDNO}&CSTNO={CSTNO}&CSTSFX={CSTSFX}&ITMID={ITMID}"

    # Retrieve username and password from Secrets Manager
    secrets = get_secret()
    Authorization = secrets['Authorization']

    # Making the API request using http.client
    conn = http.client.HTTPConnection(host, port)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': secrets['Authorization']
    }

    conn.request("GET", path, headers=headers)

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
    try:
        # Extract query parameters from the event object
        ORDNO = event.get('queryStringParameters', {}).get('ORDNO')
        CSTNO = event.get('queryStringParameters', {}).get('CSTNO')
        CSTSFX = event.get('queryStringParameters', {}).get('CSTSFX')
        ITMID = event.get('queryStringParameters', {}).get('ITMID')

        if not ORDNO or not CSTNO or not CSTSFX or not ITMID:
            return {
                "statusCode": 400,
                "body": "Missing query parameters"
            }

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






#######################################################
# DBS Dealer Lookup Script
#
# High Level Flow:
#  - Magento sends API Request for DBS to AWS API GateWay
#  - AWS API Gateway receives request and calls Lambda program
#  - This is the Lambda program that will:
#    1. examine the request
#    2. query the DynamoDB
#    3. build the target URL
#    4. Send the request to the DBS
#  - The response from the DBS will then flow back to Magento
#
# Reference: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html
#######################################################

from __future__ import print_function  # Python 2/3 compatibility

import json
import base64
import datetime

import boto3
from botocore.exceptions import ClientError
import time
import os
import requests
from requests.exceptions import HTTPError, ConnectionError

local = False
errMsg = "Missing field: [{}]"
env = os.environ['EnvName'] 

# Loads up the DynamoDB
if local:
    # For local testing
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
else:
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')  # For AWS


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': json.dumps('AWS Error: ' + str(err)) if err else json.dumps(res),
        'isBase64Encoded': 'false',
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def _get_dbs_list():
    table = dynamodb.Table('DbsAccess_' + env)
    #table = dynamodb.Table('DbsAccess')
    dbs_list = table.scan()
    return dbs_list


def _store_token(dbs_id, token, lifetime: int):
    table = dynamodb.Table('DbsAccess_' + env)
    #table = dynamodb.Table('DbsAccess')
    now = datetime.datetime.now()
    exp_date_time = now + datetime.timedelta(0, lifetime - 60)

    response = table.update_item(
        Key={'DbsId': dbs_id},
        UpdateExpression=" set AccessToken = :token, Expiration = :lifetime",
        ExpressionAttributeValues={
            ':token': token,
            ':lifetime': exp_date_time.isoformat()
        },
        ReturnValues="UPDATED_NEW"
    )

    return None


def _get_new_token(dbs_id, new_token_url, credentials, request_id):
    base_64_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    auth = 'Basic %s' % base_64_credentials
    url = new_token_url
    payload = 'grant_type=client_credentials&scope=anonymous'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json',
        'Request_Id': request_id,
        'Authorization': auth
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except ConnectionError as e:
        raise e

    json_response = json.loads(response.text.encode('utf8'))
    _store_token(dbs_id, json_response['access_token'], int(json_response['expires_in']))
    return json_response['access_token']


def _get_access_token(credentials, request_id, dbs_id, access_token, new_token_url, expiration_time):

    token_is_expired = datetime.datetime.now() > datetime.datetime.fromisoformat(expiration_time)
    if token_is_expired:
        access_token = _get_new_token(dbs_id, new_token_url, credentials, request_id)
    return access_token


def _get_secrets(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name 
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else: 
        #No binary secrets, they are all strings
        secret = get_secret_value_response['SecretString']

    secrets = json.loads(secret) 
    credentials = secrets['APIKey'] + ":" + secrets['APISecret']

    return_secrets = {
        'SubscriptionId': secrets['SubscriptionId'], 
        'Credentials': credentials
    }

    return return_secrets 


def lambda_handler(event, context):
    # Points to the 'DbsDealer' table in the DB

    table = dynamodb.Table('DbsDealer_' + env)
    #table = dynamodb.Table('DbsDealer')
    print("Event: ", json.dumps(event))
    # Read in Request
    # print("Event: ", event)
    if 'resource' in event:
        resource_path = event['resource']
        # print("Resource Path: ", resource_path)
    else:
        return respond(ValueError(errMsg.format('event->resource')))

    if 'body' in event:
        body = event['body']
        print("Body befor: ", body)
        
        body_json = json.loads(body)
        print("Body: ", body_json)
    else:
        return respond(ValueError(errMsg.format('event->body')))

    if 'DbsId' in body_json:
        dbs_id = body_json['DbsId']
        print("DbsId: ", dbs_id)
    else:
        return respond(ValueError(errMsg.format('event->body->DbsId')))

    # Note: As of Mar 2020 DealerId in Magento changed to DealerCode
    if 'DealerId' in body_json:
        dealer_id = body_json['DealerId']
        # print("DealerId: ", dealer_id)
    elif 'DealerCode' in body_json:
        dealer_id = body_json['DealerCode']
        # print("DealerId: ", dealer_id)
    elif 'OrderHistory_request_data' in body_json:
        if 'DealerCode' in body_json['OrderHistory_request_data']['Branch_Data'][0]:
            dealer_id = body_json['OrderHistory_request_data']['Branch_Data'][0]['DealerCode']
            # print("DealerId: ", dealer_id)
        else:
            return respond(
                ValueError(errMsg.format('event->body->OrderHistory_request_data->Branch_Data[0]->DealerCode')))
    elif 'BranchQuantity_request_data' in body_json:
        if 'DealerCode' in body_json['BranchQuantity_request_data']['BranchQuantity_request_data_Branches'][0]:
            dealer_id = body_json['BranchQuantity_request_data']['BranchQuantity_request_data_Branches'][0][
                'DealerCode']
            # print("DealerId: ", dealer_id) 
        else:
            return respond(ValueError(errMsg.format('event->body->BranchQuantity_request_data'
                                                    '->BranchQuantity_request_data_Branches[0]->DealerCode')))
    else:
        return respond(ValueError(errMsg.format('event->body->DealerCode')))

    if 'TransactionId' in body_json:
        transaction_id = body_json['TransactionId']
        # print("TransactionId: ", transaction_id)
    else:
        return respond(ValueError(errMsg.format('event->body->TransactionId')))

    if 'headers' in event:
        headers = event['headers']
        # print("headers: ", headers)
    else:
        return respond(ValueError(errMsg.format('event->headers')))

    # Read in DB Record
    try:
        db_response = table.get_item(
            Key={
                'DbsId': dbs_id,
                'DealerId': dealer_id
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return respond(ValueError("Unable to Search Database"))
    else:
        # print(db_response)
        # Check to see if 'Item' is returned, if not then the 'DbsId' and 'DealerId' are not defined in the DB
        if 'Item' in db_response:
            item = db_response['Item']  # Reads the item from the response
            if 'BaseUrl' in item:
                base_url = item['BaseUrl']
                # print("Base URL: ", base_url)
            else:
                return respond(
                    ValueError("BaseUrl is missing for DBS ID: {} and Dealer ID: {}".format(dbs_id, dealer_id)))
            if 'SubscriptionId'in item:
                subscription_id = item['SubscriptionId']
                print("SUBSCRIPTION: ", subscription_id)
        else:
            msg = "*****DBS ID: {} and Dealer ID: {} NOT FOUND*****".format(dbs_id, dealer_id)
            # print(msg)
            return respond(ValueError(msg))

    # Transform Endpoint
    new_url = base_url + resource_path
    # print("New URL: ", new_url)

    # Build Headers
    safe_headers = ["User-Agent", "Content-Type", "Authorization"]

    new_headers = {}
    for key, value in headers.items():
        if key in safe_headers:
            new_headers[key] = value

    # Some DBSs may have their own IDP. Authorize them here
    try:
        access_details = {}
        not_authorized_list = _get_dbs_list()
        needs_to_be_authorized = False

        for dbsDetails in not_authorized_list['Items']:
            needs_to_be_authorized = dbs_id in dbsDetails.values()
            if needs_to_be_authorized:
                access_details = dbsDetails
                break

        if needs_to_be_authorized:
            secrets = _get_secrets(access_details['SecretName'], access_details['Region'])
            accessToken = access_details.get('AccessToken', False) or None
            expiration = access_details.get('Expiration', False) or datetime.datetime.now().isoformat()
            access_token = _get_access_token(secrets['Credentials'], transaction_id, dbs_id,
                                             accessToken, access_details['NewTokenUrl'],
                                            expiration)
            new_headers['Subscription-Id'] = subscription_id
            new_headers['Request-Id'] = transaction_id
            new_headers['Authorization'] = 'Bearer ' + access_token

    except Exception as e:
        raise e
        # return respond(ValueError(e))

    print("New Headers: ", new_headers)
    # headers = {'Content-Type': 'application/json'}

    try:
        print('this is body ',body_json)
        vendor_name = dbs_id 
        start_time = time.time()
        api_response = requests.post(new_url, json=body_json, headers=new_headers, verify=False)
        duration = (time.time() - start_time) * 1000
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "vendor": vendor_name,
            "requestDuration": duration,
            "logIdentifier": "DbsAPIDealerLookup",
            "transactionId" : transaction_id,
            "resources" : event['resource']
        }
        print(json.dumps(log_entry))
        
        print('This is API Response',api_response)
        # print(dir(api_response))
        # print("API Response: ", api_response.text)
        # print("API Response Headers: ", api_response.headers)
        # print(type(api_response.headers))
        # print(dir(api_response.headers))
        # headers_dict = dict(api_response.headers)
        # print(headers_dict)
        # headers_json = json.dumps(headers_dict)
        # print(headers_json)
        # print("Response Status code: ", api_response.status_code)
        # If the response was successful, no Exception will be raised
        api_response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        #return respond(ValueError(http_err))
        return {'statusCode': api_response.status_code, 'body': api_response.text,
                'headers': {'Content-Type': 'application/json'}, 'isBase64Encoded': 'false'}
    except Exception as err:
        print(f'Other error occurred: {err}')
        return respond(ValueError(err)) 
    else:
        print('the api data return ',api_response.text)
        return {'statusCode': api_response.status_code, 'body': api_response.text,
                'headers': {'Content-Type': 'application/json'}, 'isBase64Encoded': 'false'}

