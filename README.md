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




	SELECT * FROM PPDGLOBAL."DCPP0113C" DD , 
				  PPDGLOBAL."DCPP0115" DC ,
				  ppdglobal."DEALER_MASTER" DM
	WHERE DD."ITMID" = DC."ITMID"  and  DC."CSTNO" = DM."DEALER_CODE" AND DM."DBS" = 'DSI'
