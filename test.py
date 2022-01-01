import urllib3
import json
from sys import argv

http = urllib3.PoolManager()

script, baseurl, api_key, auth_data_secret_id, auth_data_secret_key, account_id  = argv

def main():
  data = {
    "account_id": account_id,
    "access_token": nordigenAccessToken()
  }

  print("Sending request to nordigen-cache")
  response = http.request('POST', baseurl + 'nordigen-cache/', body=json.dumps(data), headers={"X-Api-Key": api_key})
  if(response.status != 200):
    response.data
    exit(1)
  else:
    print("nordigen-cache response OK!")

  print("Sending request to nordigen-cache-geturl")
  response = http.request('POST', baseurl + 'nordigen-cache-geturl/', body=json.dumps({}), headers={"X-Api-Key": api_key})
  if(response.status != 200):
    response.data
    exit(1)
  else:
    print("nordigen-cache-geturl response OK!")

  url = response.data.decode('UTF-8').strip('"')
  print("Checking S3 object")
  transactions_response = http.request('GET', url)
  transactions = json.loads(transactions_response.data.decode('UTF-8'))['transactions']
  if(not transactions):
    print("Malformed transactions response, check lambda function logs")
    exit(1)
  print("Transaction data OK!")

def nordigenAccessToken():
  auth_data = {
    "secret_id": auth_data_secret_id,
    "secret_key": auth_data_secret_key
  }

  authRequest = http.request('POST', 'https://ob.nordigen.com/api/v2/token/new/', body=json.dumps(auth_data), headers={'Accept': 'application/json', 'Content-Type': 'application/json'})
  return json.loads(authRequest.data)['access']

if __name__=="__main__":
    main()