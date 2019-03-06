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
    '-policy',
    '--policy',
    action='store_true',
    help='(Optional) - If you want to try update the policies with your new compliance standard, add this switch to the command.  Any policies not able to be updated will be listed out during the process.')

parser.add_argument(
    'source_compliance_standard_name',
    type=str,
    help='Name of the compliance standard to copy from.  Please enter it exactly as listed in the Redlock UI')

parser.add_argument(
    'destination_compliance_standard_name',
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
rl_settings = rl_lib_api.rl_jwt_get(rl_settings)[0]
print('Done.')

## Compliance Copy ##

# Check the compliance standard and get the JSON information
print('API - Getting the Compliance Standards list...', end='')
rl_settings, response_package = rl_lib_api.api_compliance_standard_list_get(rl_settings)
compliance_standard_list_temp = response_package['data']
compliance_standard_original = search_list_object_lower(compliance_standard_list_temp, 'name', args.source_compliance_standard_name)
if compliance_standard_original is None:
    rl_lib_general.rl_exit_error(400, 'Compliance Standard not found.  Please check the Compliance Standard name and try again.')
compliance_standard_new_temp = search_list_object_lower(compliance_standard_list_temp, 'name', args.destination_compliance_standard_name)
if compliance_standard_new_temp is not None:
    rl_lib_general.rl_exit_error(400, 'New Compliance Standard appears to already exist.  Please check the new Compliance Standard name and try again.')
print('Done.')

# Create the new Standard
print('API - Creating the new Compliance Standard...', end='')
compliance_standard_new_temp = {}
compliance_standard_new_temp['name'] = args.destination_compliance_standard_name
if 'description' in compliance_standard_original:
    compliance_standard_new_temp['description'] = compliance_standard_original['description']
rl_settings, response_package = rl_lib_api.api_compliance_standard_add(rl_settings, compliance_standard_new_temp)
compliance_standard_new_response = response_package['data']

# Find the new Standard object
rl_settings, response_package = rl_lib_api.api_compliance_standard_list_get(rl_settings)
compliance_standard_list_temp = response_package['data']
compliance_standard_new = search_list_object(compliance_standard_list_temp, 'name', compliance_standard_new_temp['name'])
if compliance_standard_new is None:
    rl_lib_general.rl_exit_error(500, 'New Compliance Standard was not found!  Sync error?.')
print('Done.')

# Get the list of requirements that need to be created
print('API - Getting Compliance Standard Requirements...', end='')
rl_settings, response_package = rl_lib_api.api_compliance_standard_requirement_list_get(rl_settings, compliance_standard_original['id'])
compliance_requirement_list_original = response_package['data']
print('Done.')

# Create the new requirements
print('API - Creating the Requirements and adding them to the new Standard...', end='')
for compliance_requirement_original_temp in compliance_requirement_list_original:
    compliance_requirement_new_temp = {}
    compliance_requirement_new_temp['name'] = compliance_requirement_original_temp['name']
    compliance_requirement_new_temp['requirementId'] = compliance_requirement_original_temp['requirementId']
    if 'description' in compliance_requirement_original_temp:
        compliance_requirement_new_temp['description'] = compliance_requirement_original_temp['description']
        rl_settings, response_package = rl_lib_api.api_compliance_standard_requirement_add(rl_settings, compliance_standard_new['id'], compliance_requirement_new_temp)
    compliance_requirement_new_response = response_package['data']
print('Done.')

# Get new list of requirements
print('API - Getting the new list of requirements...', end='')
rl_settings, response_package = rl_lib_api.api_compliance_standard_requirement_list_get(rl_settings, compliance_standard_new['id'])
compliance_requirement_list_new = response_package['data']
print('Done.')


# Get list of sections and create for each requirement section
print('API - Get list of sections, create them, and associate them to the new requirements (might take a while)...', end='')
# Create mapping list source for policy updates later
map_section_list = []
for compliance_requirement_original_temp in compliance_requirement_list_original:

    # Get sections for requirement
    rl_settings, response_package = rl_lib_api.api_compliance_standard_requirement_section_list_get(rl_settings, compliance_requirement_original_temp['id'])
    compliance_section_list_original_temp = response_package['data']

    # Find new ID for requirement
    compliance_requirement_new_temp = search_list_object(compliance_requirement_list_new, 'name', compliance_requirement_original_temp['name'])

    # Create new sections under new ID
    for compliance_section_original_temp in compliance_section_list_original_temp:
        compliance_section_new_temp = {}
        compliance_section_new_temp['sectionId'] = compliance_section_original_temp['sectionId']
        if 'description' in compliance_section_original_temp:
            compliance_section_new_temp['description'] = compliance_section_original_temp['description']
            rl_settings, response_package = rl_lib_api.api_compliance_standard_requirement_section_add(rl_settings, compliance_requirement_new_temp['id'], compliance_section_new_temp)
        compliance_section_new_response = response_package['data']

        # Add entry for mapping table for Policy updates later
        compliance_section_new_temp['requirementGUIDOriginal'] = compliance_requirement_original_temp['id']
        compliance_section_new_temp['requirementGUIDNew'] = compliance_requirement_new_temp['id']
        compliance_section_new_temp['sectionGUIDOriginal'] = compliance_section_original_temp['id']
        compliance_section_new_temp['sectionGUIDNew'] = None
        map_section_list.append(compliance_section_new_temp)
print('Done.')

## Policy Updates ##

# Check to see if the user wants to try to update the policies
if not args.policy:
    print('Policy switch not specified.  Skipping policy update/attach.')
else:
    # Need to add the new GUID from the new sections to the mapping tables
    print('API - Getting the new section IDs for the policy mapping and creating a map table...', end='')
    for compliance_requirement_new_temp in compliance_requirement_list_new:

        # Get new sections for requirement
        rl_settings, response_package = rl_lib_api.api_compliance_standard_requirement_section_list_get(rl_settings, compliance_requirement_new_temp['id'])
        compliance_section_list_new_temp = response_package['data']

        # Get new GUID and update mapping table
        for compliance_section_new_temp in compliance_section_list_new_temp:
            success_test = False
            for map_section_temp in map_section_list:
                if map_section_temp['requirementGUIDNew'] == compliance_requirement_new_temp['id'] and map_section_temp['sectionId'] == compliance_section_new_temp['sectionId']:
                    map_section_temp['sectionGUIDNew'] = compliance_section_new_temp['id']
                    success_test = True
                    break
            if not success_test:
                rl_lib_general.rl_exit_error(500, 'New Section cannot find related map for Policy updates!  Sync error?.')
    print('Done.')

    # Get the policy list that will need to be updated (filtered to the original standard)
    print('API - Getting the compliance standard policy list to update...', end='')
    rl_settings, response_package = rl_lib_api.api_compliance_standard_policy_list_get(rl_settings, compliance_standard_original['name'])
    policy_list_original = response_package['data']
    print('Done.')

    # Work though the list of policies to build the update package
    print('API - Individual policy retrieval and update (might take a while)...', end='')
    header_text = False
    for policy_original_temp in policy_list_original:
        # Get the individual policy JSON object
        rl_settings, response_package = rl_lib_api.api_policy_get(rl_settings, policy_original_temp['policyId'])
        policy_specific_temp = response_package['data']

        # Edit existing complianceMetadata field for update PUT
        complianceMetadata_section_list_new_temp = []
        for complianceMetadata_section_temp in policy_specific_temp['complianceMetadata']:
            complianceMetadata_section_new_temp = {}

            # Set values already in the specific policy
            if complianceMetadata_section_temp['customAssigned'] == True:
                complianceMetadata_section_new_temp['customAssigned'] = True
            else:
                complianceMetadata_section_new_temp['customAssigned'] = False
            if complianceMetadata_section_temp['systemDefault'] == True:
                complianceMetadata_section_new_temp['systemDefault'] = True
            else:
                complianceMetadata_section_new_temp['systemDefault'] = False

            # Find and set the complianceId from the policy list object
            for policy_original_complianceMetadata_temp in policy_original_temp['complianceMetadata']:
                if policy_original_complianceMetadata_temp['standardName'] == complianceMetadata_section_temp['standardName']:
                    if policy_original_complianceMetadata_temp['requirementId'] == complianceMetadata_section_temp['requirementId']:
                        if policy_original_complianceMetadata_temp['sectionId'] == complianceMetadata_section_temp['sectionId']:
                            complianceMetadata_section_new_temp['complianceId'] = policy_original_complianceMetadata_temp['complianceId']
                            break
            if 'complianceId' not in complianceMetadata_section_new_temp:
                rl_lib_general.rl_exit_error(500, 'Error matching policy specific pull with list pull!  Sync error?.')

            # Create the new existing list of complianceMetadata
            complianceMetadata_section_list_new_temp.append(complianceMetadata_section_new_temp)

        # Add new compliance section(s)
        complianceMetadata_section_list_new_temp_2 = []
        for complianceMetadata_section_temp in complianceMetadata_section_list_new_temp:
            complianceMetadata_section_new_temp = {}
            for map_section_temp in map_section_list:
                if map_section_temp['sectionGUIDOriginal'] == complianceMetadata_section_temp['complianceId']:
                    complianceMetadata_section_new_temp['customAssigned'] = True
                    complianceMetadata_section_new_temp['systemDefault'] = False
                    complianceMetadata_section_new_temp['complianceId'] = map_section_temp['sectionGUIDNew']
                    complianceMetadata_section_list_new_temp_2.append(complianceMetadata_section_new_temp)
                    break
        if len(complianceMetadata_section_list_new_temp_2) == 0:
            rl_lib_general.rl_exit_error(500, 'Cannot find any compliance section matches in a policy - this should not be possible?')

        # Merge the existing and new lists
        complianceMetadata_section_list_new_temp.extend(complianceMetadata_section_list_new_temp_2)

        # Patch in the new list to the specific policy object
        policy_specific_temp['complianceMetadata'] = complianceMetadata_section_list_new_temp

        # Post the updated policy to the API
        try:
            rl_settings, response_package = rl_lib_api.api_policy_update(rl_settings, policy_specific_temp['policyId'], policy_specific_temp)
            policy_update_response = response_package['data']
        except requests.exceptions.HTTPError as e:
            if not header_text:
                print()
                print()
                print('An error was encountered when trying to update one or more policies.  Below is a list of the policy name(s) and GUID(s) that cound not be updated.  Please manually attach these policies to your new compliance standard, if desired.')
                print('Note: The list below will build as the compliance standard is being processed.  Please wait until the "Done." at the end for the completion of processing.')
                print()
                header_text = True
            print(str(policy_specific_temp['name']) + '  ' + str(policy_specific_temp['policyId']))
    if header_text:
        print()
    print('Done.')
