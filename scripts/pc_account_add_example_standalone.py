""" Standalone Example: Add a Cloud Account """

import json

import requests

## This is an example of using the Prisma Cloud API to:
# 1. Log in using an API key (https://docs.paloaltonetworks.com/prisma/prisma-cloud/prisma-cloud-admin/manage-prisma-cloud-administrators/create-access-keys.html)
# 2. Using the resulting token from login to add a new AWS account to Prisma Cloud.
# Note: This is a very simple example to demonstrate the basic use of the API for Prisma Cloud Compute.

# Documentation of the Prisma Cloud API:
# https://api.docs.prismacloud.io/reference#login

# --Configuration-- #

PRISMA_CLOUD_API_ACCESS_KEY = 'prisma-cloud-access-key-here'
PRISMA_CLOUD_API_SECRET_KEY = 'prisma-cloud-secret-key-here'

# Cloud Account Information for the API Call (This is information about your AWS account and AWS Prisma Cloud Role).
CLOUD_TYPE                                         = 'aws'
CLOUD_ACCOUNT_ID_TO_ADD                            = 'some-aws-account-number'
CLOUD_ACCOUNT_ENABLED_FOR_SCANNING_IN_PRISMA_CLOUD = True
CLOUD_ACCOUNT_EXTERNAL_ID_FROM_AWS_ROLE            = 'external-id-used-in-the-prisma-cloud-role-in-aws'
CLOUD_ACCOUNT_ROLE_ARN_FROM_AWS                    = 'the-arn-from-the-prisma-cloud-role-created-in-aws'
PRISMA_CLOUD_ACCOUNT_GROUP_IDS                     = ['prisma-account-group-id-from-api-or-url-in-ui', 'another-prisma-account-group-id-from-api-or-url-in-ui']
PRISMA_CLOUD_ACCOUNT_FRENDLY_NAME                  = 'some-friendly-account-name-to-show-in-prisma-cloud'
PRISMA_CLOUD_MONITOR_MODE                          = 'MONITOR_AND_PROTECT'

################################

# Set the API
headers = {'Content-Type': 'application/json'}
api_url = 'https://api.prismacloud.io/login'
action  = 'POST'

# Set the POST
data = {}
data['username'] = PRISMA_CLOUD_API_ACCESS_KEY
data['password'] = PRISMA_CLOUD_API_SECRET_KEY
data_json = json.dumps(data)

# POST
response_raw = requests.request(action, api_url, headers=headers, data=data_json)
response_data = response_raw.json()
token = response_data['token']

# --Main-- #

## Example of the Add Cloud Account API

headers = {'Content-Type': 'application/json', 'x-redlock-auth': token}
api_url = 'https://api.prismacloud.io/cloud/' + CLOUD_TYPE
action  = 'POST'

# Set the POST
data = {}
data['accountId']      = CLOUD_ACCOUNT_ID_TO_ADD
data['enabled']        = CLOUD_ACCOUNT_ENABLED_FOR_SCANNING_IN_PRISMA_CLOUD
data['externalId']     = CLOUD_ACCOUNT_EXTERNAL_ID_FROM_AWS_ROLE
data['groupIds']       = PRISMA_CLOUD_ACCOUNT_GROUP_IDS
data['name']           = PRISMA_CLOUD_ACCOUNT_FRENDLY_NAME
data['protectionMode'] = PRISMA_CLOUD_MONITOR_MODE
data['roleArn']        = CLOUD_ACCOUNT_ROLE_ARN_FROM_AWS
data_json = json.dumps(data)

# POST
response_raw = requests.request(action, api_url, headers=headers, data=data_json)
print(response_raw)
