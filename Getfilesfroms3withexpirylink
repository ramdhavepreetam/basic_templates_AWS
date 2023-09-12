import boto3
import json


def get_secret_value(secret_name):
    """
    Fetch secret value from AWS Secrets Manager.
    """
    secrets_client = boto3.client('secretsmanager')
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in response:
            secret = response['SecretString']
            return json.loads(secret)
        else:
            raise ValueError("SecretString not found in the secret response")
    except Exception as e:
        raise RuntimeError(f"Unable to retrieve secret: {str(e)}")


def lambda_handler(event, context):
    s3_bucket = event['s3bucket']
    # Not used in this example, but can be incorporated as needed
    date = event['date']

    # Retrieve ExpiresIn from Secrets Manager
    secret_name = "YOUR_SECRET_NAME_HERE"
    secrets = get_secret_value(secret_name)
    if 'ExpiresIn' not in secrets:
        error_response = {
            "error": "ExpiresIn not found in secrets."
        }
        return json.dumps(error_response)
    expires_in = int(secrets['ExpiresIn'])

    # Create an S3 client
    s3 = boto3.client('s3')

    urls = []

    try:
        # List all objects in the specified bucket
        objects = s3.list_objects_v2(Bucket=s3_bucket)

        # Check if there are objects in the bucket
        if 'Contents' not in objects:
            error_response = {
                "error": "No files found in the provided location."
            }
            return json.dumps(error_response)

        for obj in objects['Contents']:
            # Generate a pre-signed URL for each object
            url = s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': s3_bucket, 'Key': obj['Key']},
                ExpiresIn=expires_in
            )
            urls.append({"Fileurl": url})

        response = {
            "Urls": urls
        }
        return json.dumps(response)

    except s3.exceptions.NoSuchBucket:
        error_response = {
            "error": "The specified bucket does not exist."
        }
        return json.dumps(error_response)

    except Exception as e:
        error_response = {
            "error": f"An error occurred: {str(e)}"
        }
        return json.dumps(error_response)
