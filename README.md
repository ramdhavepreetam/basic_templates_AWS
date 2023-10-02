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




SELECT 
    -- List the specific columns you need instead of *
    DD.someColumn,
    DC.anotherColumn,
    DM.yetAnotherColumn
FROM 
    PPDGLOBAL."DCPP0113C" DD 
JOIN 
    PPDGLOBAL."DCPP0115" DC ON DD."ITMID" = DC."ITMID"
JOIN 
    PPDGLOBAL."DEALER_MASTER" DM ON DC."CSTNO" = DM."DEALER_CODE"
WHERE 
    DM."DBS" = 'DSI';


{
  "Records": [
    {
      "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
      "receiptHandle": "MessageReceiptHandle",
      "body": "{\"dbs_code\": \"DSI\", \"filetype\": \"daily\"}",
      "attributes": {
        "ApproximateReceiveCount": "1",
        "SentTimestamp": "1523232000000",
        "SenderId": "123456789012",
        "ApproximateFirstReceiveTimestamp": "1523232000001"
      },
      "messageAttributes": {},
      "md5OfBody": "b27103d895d6dc0f1539fd0d87bfb84b",
      "eventSource": "aws:sqs",
      "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
      "awsRegion": "us-east-1"
    }
  ]
}
