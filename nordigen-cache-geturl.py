import json
import boto3
import time
from botocore.client import Config
from io import BytesIO
import os

s3 = boto3.client('s3', 'eu-west-2', config=Config(s3={'addressing_style': 'path'}))
bucket_name = os.environ['bucket_name']

def lambda_handler(event, context):
    params = json.loads(event['body'])

    f = BytesIO()

    s3.download_fileobj(bucket_name, 'ref.txt', f)

    seed = f.getvalue().decode('utf-8')

    while(not does_file_exist(seed)):
        time.sleep(1)

    url = s3.generate_presigned_url('get_object', Params = {'Bucket': bucket_name, 'Key': seed + ".json" }, ExpiresIn = 3600)

    return {
        'statusCode': 200,
        'body': json.dumps(url)
    }

def does_file_exist(seed):
    try:
        s3.head_object(Bucket=bucket_name, Key=seed + '.json')
        return True
    except:
        return False
