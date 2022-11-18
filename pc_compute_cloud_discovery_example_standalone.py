""" Standalone Example: Enable Cloud Discovery """

import json

import requests

# pylint: disable=import-error
from requests.auth import HTTPBasicAuth

## This is an example of using the Prisma Cloud Compute API to:
# 1. Add an AWS Access Key and Secret to Prisma Cloud Compute (SaaS)
# 2. Add the new Access Key to the Cloud Discovery policy.
# Note: This is a very simple example to demonstrate the basic use of the API for Prisma Cloud Compute.

# Documentation of the Prisma Cloud Compute API:
# https://cdn.twistlock.com/docs/api/twistlock_api.html

# --Configuration-- #

PRISMA_CLOUD_API_ACCESS_KEY = 'prisma-cloud-access-key-here'
PRISMA_CLOUD_API_SECRET_KEY = 'prisma-cloud-secret-key-here'

# AWS Access Key / Secret Key to add:
AWS_ACCESS_KEY = 'aws-access-key-here'
AWS_SECRET_KEY = 'aws-secret-key-here'

# Descriptive name for the Credentials in Prisma Cloud Compute.
PRISMA_CLOUD_CREDENTIAL_FRIENDLY_NAME = 'unique-descriptive-name-for-this-credential'

# Console URL for your Prisma Cloud Compute Instance.
PRISMA_CLOUD_COMPUTE_CONSOLE_URL = 'prisma-cloud-compute-console-url-here'

# API and Version URL suffix.
PRISMA_CLOUD_COMPUTE_CONSOLE_API_VERSION = '/api/v1'

# --Main-- #

# Set the API
headers = {'Content-Type': 'application/json'}
api_url = 'https://' + PRISMA_CLOUD_COMPUTE_CONSOLE_URL + PRISMA_CLOUD_COMPUTE_CONSOLE_API_VERSION + '/credentials'
action  = 'POST'

# Set the POST
data = {}
data['_id']             = PRISMA_CLOUD_CREDENTIAL_FRIENDLY_NAME
data['accountID']       = AWS_ACCESS_KEY
data['apiToken']        = {}
data['caCert']          = ''
data['secret']          = {}
data['secret']['plain'] = AWS_SECRET_KEY
data['serviceAccount']  = {}
data['type']            = 'aws'
data_json = json.dumps(data)

# POST
response_raw = requests.request(action, api_url, auth=HTTPBasicAuth(PRISMA_CLOUD_API_ACCESS_KEY, PRISMA_CLOUD_API_SECRET_KEY), headers=headers, data=data_json)
print(response_raw)

################################

## Example of the updating Policy via the Policy Update API

# Get the existing Cloud Discovery List

# Set the API
headers = {'Content-Type': 'application/json'}
api_url = 'https://' + PRISMA_CLOUD_COMPUTE_CONSOLE_URL + PRISMA_CLOUD_COMPUTE_CONSOLE_API_VERSION + '/policies/cloud-platforms'
action = 'GET'

# GET
response_raw = requests.request(action, api_url, auth=HTTPBasicAuth(PRISMA_CLOUD_API_ACCESS_KEY, PRISMA_CLOUD_API_SECRET_KEY), headers=headers)
response_data = response_raw.json()

rules_list = response_data['rules']

# Set the API
headers = {'Content-Type': 'application/json'}
api_url = 'https://' + PRISMA_CLOUD_COMPUTE_CONSOLE_URL + PRISMA_CLOUD_COMPUTE_CONSOLE_API_VERSION + '/policies/cloud-platforms'
action = 'PUT'

# Set the POST
new_policy_object = {}
new_policy_object['awsRegionType']          = 'regular'
new_policy_object['credentialId']           = PRISMA_CLOUD_CREDENTIAL_FRIENDLY_NAME
new_policy_object['discoveryEnabled']       = True
new_policy_object['roleArn']                = ''
new_policy_object['serverlessRadarEnabled'] = False
new_policy_object['vmTagsEnabled']          = False
rules_list.append(new_policy_object)
data = {}
data['rules'] = rules_list
data_json = json.dumps(data)

# POST
response_raw = requests.request(action, api_url, auth=HTTPBasicAuth(PRISMA_CLOUD_API_ACCESS_KEY, PRISMA_CLOUD_API_SECRET_KEY), headers=headers, data=data_json)
print(response_raw)
