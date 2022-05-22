import json
import boto3
import urllib3
import os

http = urllib3.PoolManager()
s3 = boto3.client('s3')


def lambda_handler(event, context):
    get_results(event['account_id'], event['access_token'], event['seed'])
    return {
        'statusCode': 200,
        'headers': {
          "Access-Control-Allow-Origin" : "*",
          "Access-Control-Allow-Credentials" : True
        },
        'body': json.dumps('Hello from Lambda!')
    }

def get_results(account_id, access_token, seed):

    response = http.request('GET', 'https://ob.nordigen.com/api/v2/accounts/' + account_id + '/transactions/', headers={"accept":"application/json", "authorization": "Bearer " + access_token})

    bucket_name = os.environ['bucket_name']
    key = seed + '.json'
    body = response.data

    s3.put_object(Bucket=bucket_name, Key=key, Body=body)