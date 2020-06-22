
## This is an example of using the Prisma Cloud API to:
# 1. Log in using an API key (https://docs.paloaltonetworks.com/prisma/prisma-cloud/prisma-cloud-admin/manage-prisma-cloud-administrators/create-access-keys.html)
# 2. Using the resulting token from login to add a new AWS account to Prisma Cloud.

# Note: This is a very simple example to demonstrate the basic use of the API for Prisma Cloud.
# For a more complex real-world example of a CLI tool built in Python for various purposes, please see the pc-toolbox example here:
# https://github.com/jdrieger/pc-toolbox

# Example of AWS onboarding toos:
# https://github.com/PaloAltoNetworks/PrismaCFNOnboarding

# Example of a bulk onboarding Terriform based tools:
# https://github.com/PaloAltoNetworks/PrismaCloud_TF_BulkOnboarding_and_AWS_Orgs

# Documentation of the Prisma Cloud API:
# https://api.docs.prismacloud.io/reference

################################

## Import Block for Modules Used ##
from __future__ import print_function
import json
import requests

################################

## Variables that would be passed in to the following API example ##
# Prisma Cloud API Key Information (from https://docs.paloaltonetworks.com/prisma/prisma-cloud/prisma-cloud-admin/manage-prisma-cloud-administrators/create-access-keys.html)
PRISMA_CLOUD_API_ACCESS_KEY_ID = "some-api-key-id-here"
PRISMA_CLOUD_API_SECRET_KEY = "some-secret-key-here"

# Cloud Account Information for the API Call (This is information about your AWS account and AWS Prisma Cloud Role)
CLOUD_TYPE = "aws"  # This will remain the same unless you want to import another type of cloud (azure, gcp, etc.)
CLOUD_ACCOUNT_ID_TO_ADD = "some-aws-account-number"
CLOUD_ACCOUNT_ENABLED_FOR_SCANNING_IN_PRISMA_CLOUD = True  # This will always be set to True unless you want to add it without scanning it
CLOUD_ACCUNT_EXTERNAL_ID_FROM_AWS_ROLE = "external-id-used-in-the-prisma-cloud-role-in-aws"
PRISMA_CLOUD_ACCOUNT_GROUP_IDS = ['prisma-account-group-id-from-api-or-url-in-ui','another-prisma-account-group-id-from-api-or-url-in-ui']  # This can be one or more Prisma Cloud Account Groups
PRISMA_CLOUD_ACCOUNT_FRENDLY_NAME = "some friendly account name to show in Prisma Cloud"
CLOUD_ACCOUNT_ROLE_ARN_FROM_AWS = "the arn from the prisma cloud role created in aws"

PRISMA_CLOUD_MONITOR_MODE = "MONITOR_AND_PROTECT"
# Valid values are either "MONITOR" or "MONITOR_AND_PROTECT"

################################

## Example of the login API call
# Detailed information can be found here: https://api.docs.prismacloud.io/reference#login

# Set the API Information to Use
headers = {'Content-Type': 'application/json'}
api_url = "https://api3.prismacloud.io/login"
action = "POST"

# Set the Login Information to get the Token as the body of the request
data = {}
data['username'] = PRISMA_CLOUD_API_ACCESS_KEY_ID
data['password'] = PRISMA_CLOUD_API_SECRET_KEY

# Convert the body data above into JSON format for the requests module
data_json = json.dumps(data)

# Make the API Call Using the requests Module with the information set above
response_raw = requests.request(action, api_url, headers=headers, data=data_json)

# Convert the response object to a more usable dictonary in Python
response_data = response_raw.json()

# Pull the token from the response package
token = response_data['token']

################################

## Example of the Add Cloud Account API
# Detailed information can be found here: https://api.docs.prismacloud.io/reference#add-cloud-account

# Set the API Information to Use (Including the token we recieved from the login above in the headers block)
headers = {'Content-Type': 'application/json', 'x-redlock-auth': token}
api_url = "https://api3.prismacloud.io/cloud/" + CLOUD_TYPE
action = "POST"

# Set the body of the request with the account information you want to add
data = {}
data['accountId'] = CLOUD_ACCOUNT_ID_TO_ADD
data['enabled'] = CLOUD_ACCOUNT_ENABLED_FOR_SCANNING_IN_PRISMA_CLOUD
data['externalId'] = CLOUD_ACCUNT_EXTERNAL_ID_FROM_AWS_ROLE
data['groupIds'] = PRISMA_CLOUD_ACCOUNT_GROUP_IDS
data['name'] = PRISMA_CLOUD_ACCOUNT_FRENDLY_NAME
data['roleArn'] = CLOUD_ACCOUNT_ROLE_ARN_FROM_AWS
data['protectionMode'] = PRISMA_CLOUD_MONITOR_MODE

# Convert the body data above into JSON format for the requests module
data_json = json.dumps(data)

# Make the API Call Using the requests Module with the information set above
response_raw = requests.request(action, api_url, headers=headers, data=data_json)

# Print the response raw package (HTTP status code) for confirmation of completion  **this can be left out if not testing**
print(response_raw)
