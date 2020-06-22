
## This is an example of using the Prisma Cloud Compute API to:
# 1. Add an AWS Access Key and Secret to Prisma Cloud Compute (SaaS)
# 2. Add the new Access Key to the Cloud Discovery policy.

# Note: This is a very simple example to demonstrate the basic use of the API for Prisma Cloud Compute.

# Documentation of the Prisma Cloud Compute API:
# https://cdn.twistlock.com/docs/api/twistlock_api.html

################################

## Import Block for Modules Used ##
from __future__ import print_function
import json
import requests
from requests.auth import HTTPBasicAuth

################################

## Variables that would be passed in to the following API example ##
# Prisma Cloud API Key Information (from https://docs.paloaltonetworks.com/prisma/prisma-cloud/prisma-cloud-admin/manage-prisma-cloud-administrators/create-access-keys.html)
# Minimum role required to access this endpoint: operator
PRISMA_CLOUD_API_ACCESS_KEY_ID = "prisma-cloud-api-key-id-here"
PRISMA_CLOUD_API_SECRET_KEY = "prisma-cloud-secret-key-here"

# AWS Access Key and Secret you wish to add:
AWS_ACCESS_KEY_ID = "aws-access-key-id-here"
AWS_ACCESS_KEY_SECRET = "aws-access-key-secret-here"

# Friendly name for the credential in Prisma Cloud:
PRISMA_CLOUD_CREDENTIAL_FRIENDLY_NAME = "some-unique-friendly-name-for-this-credential"

# Console URL for your Prisma Cloud Compute Instance
PRISMA_CLOUD_COMPUTE_CONSOLE_URL = "replace-this-example-us-east1.cloud.twistlock.com/us-1-5555121212"

# API and version URL addon (At this time, there is only V1 so this is static at this time)
PRISMA_CLOUD_COMPUTE_CONSOLE_API_VERSION = "/api/v1"


################################

## Example of the Credential Add API Call
# Detailed information can be found here: https://cdn.twistlock.com/docs/api/twistlock_api.html

# Set the API Information to Use
headers = {'Content-Type': 'application/json'}
api_url = "https://" + PRISMA_CLOUD_COMPUTE_CONSOLE_URL + PRISMA_CLOUD_COMPUTE_CONSOLE_API_VERSION + "/credentials"
action = "POST"

# Set the body of the request for the POST
data = {}
data['caCert'] = ""
data['secret'] = {}
data['secret']['plain'] = AWS_ACCESS_KEY_SECRET
data['serviceAccount'] = {}
data['apiToken'] = {}
data['type'] = "aws"
data['_id'] = PRISMA_CLOUD_CREDENTIAL_FRIENDLY_NAME
data['accountID'] = AWS_ACCESS_KEY_ID

# Convert the body data above into JSON format for the requests module
data_json = json.dumps(data)

# Make the API Call Using the requests Module with the information set above
response_raw = requests.request(action, api_url, auth=HTTPBasicAuth(PRISMA_CLOUD_API_ACCESS_KEY_ID, PRISMA_CLOUD_API_SECRET_KEY), headers=headers, data=data_json)


################################

## Example of the updating policy via the Policy Update API for Cloud Discovery for AWS
# Detailed information can be found here: https://cdn.twistlock.com/docs/api/twistlock_api.html

## Get the existing Cloud Discovery List
# Set the API Information to Use
headers = {'Content-Type': 'application/json'}
api_url = "https://" + PRISMA_CLOUD_COMPUTE_CONSOLE_URL + PRISMA_CLOUD_COMPUTE_CONSOLE_API_VERSION + "/policies/cloud-platforms"
action = "GET"

# Make the API Call Using the requests Module with the information set above
response_raw = requests.request(action, api_url, auth=HTTPBasicAuth(PRISMA_CLOUD_API_ACCESS_KEY_ID, PRISMA_CLOUD_API_SECRET_KEY), headers=headers)

# Grab the resulting content from the HTTPS request
response_data = response_raw.json()

# Pull the token from the response package to be used in the PUT API call next
rules_list = response_data['rules']

## Add the new credential to the policy
# Set the API Information to Use
headers = {'Content-Type': 'application/json'}
api_url = "https://" + PRISMA_CLOUD_COMPUTE_CONSOLE_URL + PRISMA_CLOUD_COMPUTE_CONSOLE_API_VERSION + "/policies/cloud-platforms"
action = "PUT"

# Create the new rule data structure you want to add to the exisitng list
new_policy_object = {}
new_policy_object['credentialId'] = PRISMA_CLOUD_CREDENTIAL_FRIENDLY_NAME
new_policy_object['roleArn'] = ""
new_policy_object['awsRegionType'] = "regular"
new_policy_object['discoveryEnabled'] = True
new_policy_object['vmTagsEnabled'] = False
new_policy_object['serverlessRadarEnabled'] = False

# Add the new object to the existing list
rules_list.append(new_policy_object)

# Add the new rules list into the policy update
data = {}
data['rules'] = rules_list

# Convert the body data above into JSON format for the requests module
data_json = json.dumps(data)

# Make the API Call Using the requests Module with the information set above
response_raw = requests.request(action, api_url, auth=HTTPBasicAuth(PRISMA_CLOUD_API_ACCESS_KEY_ID, PRISMA_CLOUD_API_SECRET_KEY), headers=headers, data=data_json)

# Print the response raw package (HTTP status code) for confirmation of completion  **this can be left out if not testing**
print(response_raw)
