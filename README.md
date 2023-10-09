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



import pymysql  
import sys  
import json  
import config  
import boto3  
  
  
def get_values(ORDNO, CSTNO, CSTSFX, ITMID): 
     #Db connections for rds  
    REGION=config.data["REGION"]  
    rds_host=config.data["rds_host"]  
    username=config.data["username"]  
    password=config.data["password"]  
    db_name=config.data["db_name"]  
    conn = pymysql.connect(rds_host, username, password, db_name, connect_timeout=5)  
     
    final = {}   
    final.setdefault('result', [])   
    with conn.cursor() as curr:   
        query ="SELECT distinct DOPORDM0.ORDNO,DOPORDM0.CSTNO,DOPORDM0.CSTSFX,DOPORDM3.ITMID,DCSCIM.ITMDESC,DOPORDM3.ORDLN,DOPORDM3.CUSTLN,DOPORDM4.RELNO,DOPORDM4.SEQ,DOPORDM3.CSTSKU, DOPORDM3.STAT,DWMPQSH.FRTCRY as PDC_Carrier, DOPORDM0.CSTORD,date_format(DPMORDM0.ISSDTE,'%%m/%%d/%%Y') as ISSDTE,date_format(DPMORDM3.PROMDTE,'%%m/%%d/%%Y')as PROMDTE,DPMORDM3.POLNNBR,DOPORDM3.QTYBO,DOPORDM3.QTYFUTR,DOPORDM3.QTYALC,DOPORDM3.QTYPICKED,DOPORDM3.QTYSHP,DOPORDM3.QTYINV,DOPORDM3.UOM,DOPORDM3.QTYCNL,Case When substr(DOPORDM0.DISTCTR,1,1)='X' Then 'Y' When substr(DOPORDM0.DISTCTR,1,1)<>'X' and DOPORDM0.ORDTYP='TD' then 'Y' When substr(DCSCTMR.RECD,90,1) = 'Y' then 'Y' ELSE 'N' End AS DSP_ORDER,date_format(DOPORDM4.DTESHP,'%%m/%%d/%%Y')as DTESHP,DPMREQ.PONBR,CASE WHEN DOPORDM3.VNDID = ' ' THEN DCSCIM.VNDID ELSE DOPORDM3.VNDID END AS VNDID,CASE WHEN DOPORDM3.VNDID = ' ' THEN DCSCIM.VNDSFX ELSE DOPORDM3.VNDSFX END AS VNDSFX,DOPORDM4.INVOICE,DOPORDM3.QTYORD,DWMPQSH.PRONO as PDCTracking,Coalesce((Select count(Distinct(cmt)) from DOPORDM2 where DOPORDM2.ORDNO=DOPORDM0.ORDNO and DOPORDM2.CSTNO=DOPORDM0.CSTNO and DOPORDM2.ORDLN=DOPORDM3.ORDLN and DOPORDM2.CSTSFX=DOPORDM0.CSTSFX and DOPORDM2.RCDTYP='I'),0) as CMTCTR,Coalesce((Select count(Distinct(DPMORDM2A.Desc)) from DPMORDM2A where DPMORDM2A.PONBR=DPMREQ.PONBR and DPMORDM2A.POLNNBR=DPMREQ.POLNNBR),0) as PONoteCtr FROM (DOPORDM0 join DOPORDM3 on DOPORDM0.ORDNO=DOPORDM3.ORDNO and DOPORDM0.CSTNO=DOPORDM3.CSTNO and DOPORDM0.CSTSFX=DOPORDM3.CSTSFX) left join DOPORDM4 on DOPORDM4.ORDNO=DOPORDM3.ORDNO and DOPORDM4.ORDLN=DOPORDM3.ORDLN and DOPORDM4.CSTNO=DOPORDM3.CSTNO and  DOPORDM4.CSTSFX=DOPORDM3.CSTSFX left join DWMPQSH on DOPORDM4.DISTCTR=DWMPQSH.DISTCTR and DOPORDM4.CSTNO=DWMPQSH.CSTNO and DOPORDM4.CSTSFX=DWMPQSH.CSTSFX and DOPORDM4.BOXNO=DWMPQSH.BOXNO left join DPMREQ on DPMREQ.REQNBR=DOPORDM3.REQNBR and DPMREQ.ORGSYS='COPS' and DPMREQ.ORGNBR=DOPORDM0.ORDNO left join DCSCIM on DOPORDM3.ITMID=DCSCIM.ITMID left join DPMORDM0 on DPMREQ.PONBR=DPMORDM0.PONBR left join DPMORDM3 on DPMORDM0.PONBR=DPMORDM3.PONBR and DPMREQ.POLNNBR=DPMORDM3.POLNNBR and DOPORDM3.ITMID=DPMORDM3.ITMID left join DCSCTMR on DCSCTMR.TBLID=617 and DCSCTMR.SUFFIX=substr(DOPORDM3.ORDNO,1,2) Where DOPORDM0.ORDNO=%s and DOPORDM0.CSTNO=%s and  DOPORDM0.CSTSFX=%s and DOPORDM3.ITMID= %s"
        curr.execute(query,(ORDNO,CSTNO,CSTSFX,ITMID))    
        result =curr.fetchall() 
        for row in range(len(result)):   
            if result[row][0]==None:   
                ORDNO =''   
            else:   
                ORDNO = str(result[row][0])   
                   
            if result[row][1]==None:   
                CSTNO =''   
            else:   
                CSTNO = str(result[row][1])   
               
            if result[row][2]==None:   
                CSTSFX =''   
            else:   
                CSTSFX = str(result[row][2])   
               
            if result[row][3]==None:   
                ITMID =''   
            else:   
                ITMID = str(result[row][3])   
               
            if result[row][4]==None:   
                ITMDESC =''   
            else:   
                ITMDESC = str(result[row][4])   
            if result[row][5]==None or '':   
                ORDLN = 0   
            else:   
                ORDLN = int(result[row][5])   
            if result[row][6]==None or '':   
                CUSTLN = 0   
            else:   
                CUSTLN = int(result[row][6])   
            if result[row][7]==None or '':   
                RELNO = 0   
            else:   
                RELNO = int(result[row][7])   
            if result[row][8]==None or '':   
                SEQ = 0   
            else:   
                SEQ = int(result[row][8])   
            if result[row][9]==None:   
                CSTSKU =''   
            else:   
                CSTSKU = str(result[row][9])   
            if result[row][10]==None:   
                STAT =''   
            else:   
                STAT = str(result[row][10])   
            if result[row][11]==None:   
                PDC_Carrier=''   
            else:   
                PDC_Carrier = str(result[row][11])   
            if result[row][12]==None:   
                CSTORD=''   
            else:   
                CSTORD = str(result[row][12])   
            if result[row][13]==None or result[row][13]=='00/00/0000':   
                ISSDTE =''   
            else:   
                ISSDTE = str(result[row][13])   
            if result[row][14]==None or result[row][14]=='00/00/0000':   
                PROMDTE =''   
            else:   
                PROMDTE = str(result[row][14])   
            if result[row][15]==None:   
                POLNNBR =''   
            else:   
                POLNNBR = str(result[row][15])   
            if result[row][16]==None or '':   
                QTYBO = 0   
            else:   
                QTYBO=int(result[row][16])   
            if result[row][17]==None or '':   
                QTYFUTR = 0   
            else:   
                QTYFUTR = int(result[row][17])   
            if result[row][18]==None or '':   
                QTYALC = 0   
            else:   
                QTYALC = int(result[row][18])   
            if result[row][19]==None or '':   
                QTYPICKED = 0   
            else:   
                QTYPICKED = int(result[row][19])   
            if result[row][20]==None or '':   
                QTYSHP = 0   
            else:   
                QTYSHP = int(result[row][20])   
            if result[row][21]==None or '':   
                QTYINV = 0   
            else:   
                QTYINV = int(result[row][21])   
            if result[row][22]==None:   
                UOM = 0   
            else:   
                UOM = result[row][22]   
            if result[row][23]==None or '':   
                QTYCNL = 0   
            else:   
                QTYCNL = int(result[row][23])  
            if result[row][24]==None:   
                DSP_ORDER = ''  
            else:   
                DSP_ORDER = str(result[row][24])  
            if result[row][25]==None or '' or result[row][25]=='00/00/0000':   
                DTESHP =''   
            else:   
                DTESHP = result[row][25]   
            if result[row][26]==None:   
                PONBR =''   
            else:   
                PONBR = str(result[row][26])   
            if result[row][27]==None:   
                VNDID =''   
            else:   
                VNDID = str(result[row][27])   
            if result[row][28]==None:   
                VNDSFX =''   
            else:   
                VNDSFX = str(result[row][28])   
            if result[row][29]==None or '':   
                INVOICE = 0   
            else:   
                INVOICE = int(result[row][29])   
            if result[row][30]==None or '':   
                QTYORD = 0   
            else:   
                QTYORD= int(result[row][30])   
            if result[row][31]==None:   
                PDCTracking =''   
            else:   
                PDCTracking = str(result[row][31])   
            if result[row][32]==None or '':   
                CMTCTR = 0   
            else:   
                CMTCTR =int(result[row][32])   
            if result[row][33]==None or'':   
                PONoteCtr = 0   
            else:   
                PONoteCtr =int(result[row][33])   
   
            y = {   
                'ORDNO': ORDNO,   
                'CSTNO': CSTNO,   
                'CSTSFX': CSTSFX,   
                'ITMID': ITMID,   
                'ITMDESC': ITMDESC,   
                'ORDLN': ORDLN,   
                'CUSTLN': CUSTLN,   
                'RELNO': RELNO,   
                'SEQ': SEQ,   
                'CSTSKU': CSTSKU,   
                'STAT': STAT,   
                'PDC_Carrier':PDC_Carrier,   
                'CSTORD': CSTORD,   
                'ISSDTE': ISSDTE,   
                'PROMDTE': PROMDTE,   
                'POLNNBR': POLNNBR,   
                'QTYBO':QTYBO,   
                'QTYFUTR':QTYFUTR,   
                'QTYALC':QTYALC,   
                'QTYPICKED':QTYPICKED,   
                'QTYSHP':QTYSHP,   
                'QTYINV':QTYINV,   
                'UOM': UOM,   
                'QTYCNL': QTYCNL,  
                'DSP_ORDER':DSP_ORDER,  
                'DTESHP': DTESHP,   
                'PONBR' : PONBR,   
                'VNDID':VNDID,   
                'VNDSFX':VNDSFX,   
                'INVOICE':INVOICE,   
                'QTYORD':QTYORD,   
                'PDCTracking':PDCTracking,   
                'CMTCTR': CMTCTR,   
                'PONoteCtr': PONoteCtr,   
            }   
            final['result'].append(y)     
        curr.close()     
    conn.close()    
    return final['result']   
       
      
def lambda_handler(event, context):   
    ORDNO = event['queryStringParameters']['ORDNO']   
    CSTNO = event['queryStringParameters']['CSTNO']   
    CSTSFX = event['queryStringParameters']['CSTSFX']   
    ITMID = event['queryStringParameters']['ITMID']   
    result=get_values(ORDNO, CSTNO, CSTSFX, ITMID)   
       
       
   
    if result == 'ERROR':   
        return {   
            "statusCode": 500,   
            "body": "Server Error",   
       
        }   
    else:   
        return {   
            "statusCode": 200,   
            "body": json.dumps(result),   
        }   
  
{   
    "ORDNO": "XSRN919",
    "CSTNO":"B400",
    "CSTSFX":" ",
    "ITMID": "21-10F0"
}



http://ppdtest:10010/web/services/RetrieveOrderInfo


{
    "OutData": {
        "OutDataS": [
            {
                "ORDNO": "XSRN919",
                "CSTNO": "B400",
                "CSTSFX": "",
                "ITMID": "21-10F0",
                "ITMDESC": "SYSTEM-SPACEMASTER 10 PNL 81-8 ADD EXPL",
                "SALEIND": "Y",
                "ORDLN": 1,
                "CUSTLN": 1,
                "RELNO": 1,
                "SEQ": 0,
                "CSTSKU": "",
                "STAT": "6",
                "PDC_CARRIER": "",
                "CSTORD": "TEST PO A 10286AA",
                "ISSDTE": "01/16/23",
                "PROMDTE": "01/18/23",
                "POLNNBR": 1,
                "QTYBO": 0.0000,
                "QTYFUTR": 0.0000,
                "QTYALC": 0.0000,
                "QTYPICKED": 0.0000,
                "QTYSHP": 15.0000,
                "QTYINV": 0.0000,
                "UOM": "EA",
                "QTYCNL": 0.0000,
                "DSP_ORDER": "Y",
                "DTESHP": "02/27/23",
                "PONBR": "XS-XU72838",
                "VNDID": "10286AA",
                "VNDSFX": "",
                "INVOICE": 0,
                "QTYORD": 15.0000,
                "PDCTRACKING": "",
                "CMTCTR": 2,
                "PONOTECTR": 3,
                "ENDCSTNAM": ""
            }
        ]
    },
    "ErrorResponse": {
        "IsSuccess": "true",
        "ErrorMessages": []
    }
}







        [ERROR]	2023-10-05T17:26:38.277Z	0affed40-2cab-49cf-9951-7c56e04459b7	Unexpected error: list_all_objects() missing 1 required positional argument: 'prefix'
