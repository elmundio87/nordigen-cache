# nordigen-cache
Asynchronously fetch data from the Nordigen Transaction API using AWS Lambda functions.

Nordigen provides an API abstraction layer for a wide array of banking institutions that support the Open Banking API standards.

## Why did you make this?

I use Nordigen to fetch my pending credit card transactions via iOS Shortcuts - unfortunately, Shortcuts does not support asynchronous workflows, all actions must happen concurrently.

To work around this, I use the nordigen-cache Lamdda function to fetch the transaction data asynchronously at the beginning of a Shortcut. 
The data is stored in Amazon S3 until it's fetched later by calling the nordigen-cache-geturl function.

This is for my personal use only and should not be used in Production systems.

For more information on how to generate Nordigen inputs, refer to the [API documentation](https://nordigen.com/en/account_information_documenation/integration/quickstart_guide/)

IMPORTANT: Ensure that all API Gateway endpoints are protected by an API Key or similar

## Usage:

### Trigger Asynchronous fetch

Send a POST request to the nordigen-cache's API Gateway endpoint with the following body attributes:

|Attribute |Description  | Type|
--- | --- | ---|
|account_id|The Nordigen account ID to query |String|
|access_token|A valid Nordigen access token|String|

### Fetch results from S3

Send a POST request to the nordigen-cache-geturl API Gateway endpoint.

This will return a presigned URL to the latest transaction data stored in S3. 

Fetch the contents of this URL to access the transaction data.
