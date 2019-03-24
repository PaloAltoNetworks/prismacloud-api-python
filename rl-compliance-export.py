from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import argparse
import rl_lib_api
import rl_lib_general
import requests


# --Helper Functions (Local)-- #
def search_list_value(list_to_search, field_to_search, field_to_return, search_value):
    item_to_return = None
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search] == search_value:
                item_to_return = source_item[field_to_return]
                break
    return item_to_return


def search_list_value_lower(list_to_search, field_to_search, field_to_return, search_value):
    item_to_return = None
    search_value = search_value.lower()
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search].lower() == search_value:
                item_to_return = source_item[field_to_return]
                break
    return item_to_return


def search_list_object(list_to_search, field_to_search, search_value):
    object_to_return = None
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search] == search_value:
                object_to_return = source_item
                break
    return object_to_return


def search_list_object_lower(list_to_search, field_to_search, search_value):
    object_to_return = None
    search_value = search_value.lower()
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search].lower() == search_value:
                object_to_return = source_item
                break
    return object_to_return


def search_list_list(list_to_search, field_to_search, search_value):
    object_list_to_return = []
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search] == search_value:
                object_list_to_return.append(source_item)
                break
    return object_list_to_return


def search_list_list_lower(list_to_search, field_to_search, search_value):
    object_list_to_return = []
    search_value = search_value.lower()
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search].lower() == search_value:
                object_list_to_return.append(source_item)
                break
    return object_list_to_return


# --Execution Block-- #
# --Parse command line arguments-- #
parser = argparse.ArgumentParser(prog='rltoolbox')

parser.add_argument(
    '-u',
    '--username',
    type=str,
    help='*Required if no settings file has been created* - Redlock API UserName that you want to set to access your Redlock account.')

parser.add_argument(
    '-p',
    '--password',
    type=str,
    help='*Required if no settings file has been created* - Redlock API password that you want to set to access your Redlock account.')

parser.add_argument(
    '-c',
    '--customername',
    type=str,
    help='*Required if no settings file has been created* - Name of the Redlock account to be used.')

parser.add_argument(
    '-url',
    '--uiurl',
    type=str,
    help='*Required if no settings file has been created* - Base URL used in the UI for connecting to Redlock.  '
         'Formatted as app.redlock.io or app2.redlock.io or app.eu.redlock.io, etc.')

parser.add_argument(
    '-y',
    '--yes',
    action='store_true',
    help='(Optional) - Override user input for verification (auto answer for yes).')

parser.add_argument(
    'source_compliance_standard_name',
    type=str,
    help='Name of the compliance standard to copy from.  Please enter it exactly as listed in the Redlock UI')

parser.add_argument(
    'export_file_name',
    type=str,
    help='Name of the new compliance standard to create.')

args = parser.parse_args()
# --End parse command line arguments-- #

# --Main-- #
# Get login details worked out
rl_settings = rl_lib_general.rl_login_get(args.username, args.password, args.customername, args.uiurl)

# Verification (override with -y)
if not args.yes:
    print()
    print('This action will be done against the customer account name of "' + rl_settings['customerName'] + '".')
    verification_response = str(input('Is this correct (y or yes to continue)?'))
    continue_response = {'yes', 'y'}
    print()
    if verification_response not in continue_response:
        rl_lib_general.rl_exit_error(400, 'Verification failed due to user response.  Exiting...')

# Sort out API Login
print('API - Getting authentication token...', end='')
rl_settings = rl_lib_api.rl_jwt_get(rl_settings)
print(' Done.')

## Compliance Copy ##
export_file_data = {}
export_file_data['export_file_version'] = 1
export_file_data['compliance_section_list_original'] = {}
export_file_data['policy_object_original'] = {}

# Check the compliance standard and get the JSON information
print('API - Getting the Compliance Standards list...', end='')
rl_settings, response_package = rl_lib_api.api_compliance_standard_list_get(rl_settings)
compliance_standard_list_temp = response_package['data']
compliance_standard_original = search_list_object_lower(compliance_standard_list_temp, 'name', args.source_compliance_standard_name)
if compliance_standard_original is None:
    rl_lib_general.rl_exit_error(400, 'Compliance Standard not found.  Please check the Compliance Standard name and try again.')
export_file_data['compliance_standard_original'] = compliance_standard_original
print(' Done.')

# Get the list of requirements that need to be exported
print('API - Getting Compliance Standard Requirements...', end='')
rl_settings, response_package = rl_lib_api.api_compliance_standard_requirement_list_get(rl_settings, compliance_standard_original['id'])
compliance_requirement_list_original = response_package['data']
export_file_data['compliance_requirement_list_original'] = compliance_requirement_list_original
print(' Done.')

# Get list of sections and export for each requirement section
print('API - Get list of sections...', end='')
for compliance_requirement_original_temp in compliance_requirement_list_original:

    # Get sections for requirement
    rl_settings, response_package = rl_lib_api.api_compliance_standard_requirement_section_list_get(rl_settings, compliance_requirement_original_temp['id'])
    compliance_section_list_original_temp = response_package['data']
    export_file_data['compliance_section_list_original'][compliance_requirement_original_temp['id']] = compliance_section_list_original_temp
print(' Done.')

# Get the associated policies
print('API - Getting the compliance standard policy list...', end='')
rl_settings, response_package = rl_lib_api.api_compliance_standard_policy_list_get(rl_settings, compliance_standard_original['name'])
policy_list_original = response_package['data']
export_file_data['policy_list_original'] = policy_list_original
print(' Done.')

# Get the individual policy objects in case something needs to be added for import
print('API - Individual policy retrieval (might take a while)...', end='')
for policy_original_temp in policy_list_original:
    # Get the individual policy JSON object
    rl_settings, response_package = rl_lib_api.api_policy_get(rl_settings, policy_original_temp['policyId'])
    policy_specific_temp = response_package['data']
    export_file_data['policy_object_original'][policy_original_temp['policyId']] = policy_specific_temp
print(' Done.')

# Save compliance standard to file
print('FILE - Saving Compliance Standard to a file...', end='')
rl_lib_general.rl_file_write_json(args.export_file_name, export_file_data)
print(' File saved to ' + args.export_file_name)
