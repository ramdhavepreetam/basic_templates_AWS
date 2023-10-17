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



