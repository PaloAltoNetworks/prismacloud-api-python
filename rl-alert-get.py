from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import argparse
import rl_lib_api
import rl_lib_general
import json


# --Execution Block-- #
# --Parse command line arguments-- #
parser = argparse.ArgumentParser(prog='rltoolbox')

parser.add_argument(
    '-u',
    '--username',
    type=str,
    help='*Required* - Prisma Cloud API Access Key ID that you want to set to access your Prisma Cloud account.')

parser.add_argument(
    '-p',
    '--password',
    type=str,
    help='*Required* - Prisma Cloud API Secret Key that you want to set to access your Prisma Cloud account.')

parser.add_argument(
    '-url',
    '--uiurl',
    type=str,
    help='*Required* - Base URL used in the UI for connecting to Prisma Cloud.  '
         'Formatted as app.prismacloud.io or app2.prismacloud.io or app.eu.prismacloud.io, etc.  '
         'You can also input the api version of the URL if you know it and it will be passed through.')

parser.add_argument(
    '-y',
    '--yes',
    action='store_true',
    help='(Optional) - Override user input for verification (auto answer for yes).')

parser.add_argument(
    '--detailed',
    action='store_true',
    help='(Optional) - Detailed alerts response.')

parser.add_argument(
    '-fas',
    '--alertstatus',
    type=str,
    help='(Optional) - Filter - Alert Status.')

parser.add_argument(
    '-fpt',
    '--policytype',
    type=str,
    help='(Optional) - Filter - Policy Type.')

parser.add_argument(
    '-tr',
    '--timerange',
    type=int,
    default=30,
    help='(Optional) - Time Range in days.  Defaults to 30.')

parser.add_argument(
    '-l',
    '--limit',
    type=int,
    default=500,
    help='(Optional) - Return values limit (Default to 500).')


args = parser.parse_args()
# --End parse command line arguments-- #

#### Example of using the v2 alerts API call with a filter ####

# --Main-- #
# Get login details worked out
rl_settings = rl_lib_general.rl_login_get(args.username, args.password, args.uiurl)

# Verification (override with -y)
if not args.yes:
    print()
    print('Ready to excute commands aginst your Prisma Cloud tenant.')
    verification_response = str(input('Would you like to continue (y or yes to continue)?'))
    continue_response = {'yes', 'y'}
    print()
    if verification_response not in continue_response:
        rl_lib_general.rl_exit_error(400, 'Verification failed due to user response.  Exiting...')

# Sort out API Login
print('API - Getting authentication token...', end='')
rl_settings = rl_lib_api.rl_jwt_get(rl_settings)
print('Done.')

# Sort out and built the filters JSON
print('Local - Building the filter JSON package...', end='')
alerts_filter = {}

if args.detailed:
    alerts_filter['detailed'] = True
else:
    alerts_filter['detailed'] = False

alerts_filter['timeRange'] = {}
alerts_filter['timeRange']['type'] = "relative"
alerts_filter['timeRange']['value'] = {}
alerts_filter['timeRange']['value']['unit'] = "day"
alerts_filter['timeRange']['value']['amount'] = args.timerange

alerts_filter['sortBy'] = ["id:asc"]

alerts_filter['offset'] = 0

alerts_filter['limit'] = args.limit

alerts_filter['filters'] = []
if args.alertstatus is not None:
    temp_filter = {}
    temp_filter['operator'] = "="
    temp_filter['name'] = "alert.status"
    temp_filter['value'] = args.alertstatus
    alerts_filter['filters'].append(temp_filter)
if args.policytype is not None:
    temp_filter = {}
    temp_filter['operator'] = "="
    temp_filter['name'] = "policy.type"
    temp_filter['value'] = args.policytype
    alerts_filter['filters'].append(temp_filter)

print('Done.')


# Get alerts list
print('API - Getting alerts list...', end='')
rl_settings, response_package = rl_lib_api.api_alert_v2_list_get(rl_settings, data=alerts_filter)
alerts_list = response_package['data']
print('Done.')

# Print the list to the screen
print()
print(json.dumps(alerts_list))
