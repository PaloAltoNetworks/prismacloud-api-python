from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import argparse
import pc_lib_api
import pc_lib_general


# --Configuration-- #
# Import file version expected
DEFAULT_POLICY_EXPORT_FILE_VERSION = 2


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
    'export_file_name',
    type=str,
    help='Name of the export file to store the policy data.')

args = parser.parse_args()
# --End parse command line arguments-- #

# --Main-- #
# Get login details worked out
pc_settings = pc_lib_general.pc_login_get(args.username, args.password, args.uiurl)

# Verification (override with -y)
if not args.yes:
    print()
    print('Ready to excute commands aginst your Prisma Cloud tenant.')
    verification_response = str(input('Would you like to continue (y or yes to continue)?'))
    continue_response = {'yes', 'y'}
    print()
    if verification_response not in continue_response:
        pc_lib_general.pc_exit_error(400, 'Verification failed due to user response.  Exiting...')

# Sort out API Login
print('API - Getting authentication token...')
pc_settings = pc_lib_api.pc_jwt_get(pc_settings)
print(' Done.')
print()

## Policy Export ##

# Build the export file data structure
export_file_data = {}
export_file_data['export_file_version'] = DEFAULT_POLICY_EXPORT_FILE_VERSION
export_file_data['policy_object_original'] = {}
export_file_data['search_object_original'] = {}
export_file_data['policy_list_original'] = []

# Get the custom policies to export
print('API - Getting the custom policy list...')
pc_settings, response_package = pc_lib_api.api_policy_custom_v2_list_get(pc_settings)
policy_list_original = response_package['data']
export_file_data['policy_list_original'] = policy_list_original
print(' Done.')
print()

# Get the individual policy objects in case something needs to be added for import
print('API - Individual policy retrieval (might take a while)...')
for policy_original_temp in policy_list_original:
    # Get the individual policy JSON object
    print("Exporting: " + policy_original_temp['name'])
    pc_settings, response_package = pc_lib_api.api_policy_get(pc_settings, policy_original_temp['policyId'])
    policy_specific_temp = response_package['data']
    export_file_data['policy_object_original'][policy_original_temp['policyId']] = policy_specific_temp
    # Get the related saved search object (if needed)
    if 'savedSearch' in policy_original_temp['rule']['parameters']:
        if policy_original_temp['rule']['parameters']['savedSearch'] == "true":
            if policy_original_temp['rule']['criteria'] not in export_file_data['search_object_original']:
                pc_settings, response_package = pc_lib_api.api_search_get(pc_settings, policy_original_temp['rule']['criteria'])
                search_specific_temp = response_package['data']
                export_file_data['search_object_original'][policy_original_temp['rule']['criteria']] = search_specific_temp
print(' Done.')
print()

# Save policies to file
print('FILE - Saving Custom Policies to a file...')
pc_lib_general.pc_file_write_json(args.export_file_name, export_file_data)
print(' File saved to ' + args.export_file_name)
print()
