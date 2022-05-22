import json
import boto3
import random
import string
import typing
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):

    seed = get_random_string(24)

    bucket_name = os.environ['bucket_name']
    key = 'ref.txt'
    body = seed

    params = json.loads(event['body'])


    s3.put_object(Bucket=bucket_name, Key=key, Body=body)
    lambdaInput = { "account_id": params["account_id"], "access_token": params["access_token"], "seed": seed }
    invokeLambdaFunction(functionName='nordigen-cache-async',  payload=lambdaInput)

    return {
        'statusCode': 200,
        'headers': {
          "Access-Control-Allow-Origin" : "*",
          "Access-Control-Allow-Credentials" : True
        },
        'body': json.dumps(seed)
    }

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def invokeLambdaFunction(*, functionName:str=None, payload:typing.Mapping[str, str]=None):
    if  functionName == None:
        raise Exception('ERROR: functionName parameter cannot be NULL')
    payloadStr = json.dumps(payload)
    payloadBytesArr = bytes(payloadStr, encoding='utf8')
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName=functionName,
        InvocationType="Event",
        Payload=payloadBytesArr
    )
    return response
