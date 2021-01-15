from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import pc_lib_api
import pc_lib_general
import json
import requests
import time


# --Configuration-- #
# Import file version expected
DEFAULT_COMPLIANCE_IMPORT_FILE_VERSION = 3
WAIT_TIMER = 5


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
parser = pc_lib_general.pc_arg_parser_defaults()

parser.add_argument(
    '-policy',
    '--policy',
    action='store_true',
    help='(Optional) - If you want to try update the policies with your new compliance standard, add this switch to the command.')

parser.add_argument(
    '-label',
    '--label',
    action='store_true',
    help='(Optional) - Add a label to any policy updated with the new compliance standard.  This only works if you have also specified the -policy switch.')

parser.add_argument(
    'source_import_file_name',
    type=str,
    help='Name of the file to import the new compliance standard from.')

parser.add_argument(
    'destination_compliance_standard_name',
    type=str,
    help='Name of the new compliance standard to create.')

args = parser.parse_args()
# --End parse command line arguments-- #

# --Main-- #
# Get login details worked out
pc_settings = pc_lib_general.pc_login_get(args.username, args.password, args.uiurl, args.config_file)

# Verification (override with -y)
if not args.yes:
    print()
    print('Ready to execute commands against your Prisma Cloud tenant.')
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

## Compliance Copy ##
# Read in the JSON import file
export_file_data = pc_lib_general.pc_file_read_json(args.source_import_file_name)

# Do a quick validation to see if we are getting the base keys
if 'compliance_standard_original' not in export_file_data:
    pc_lib_general.pc_exit_error(404, 'Data imported from file appears corrupt or incorrect for this operation.  Please check the import file name.')
if 'compliance_requirement_list_original' not in export_file_data:
    pc_lib_general.pc_exit_error(404, 'Data imported from file appears corrupt or incorrect for this operation.  Please check the import file name.')
if 'compliance_section_list_original' not in export_file_data:
    pc_lib_general.pc_exit_error(404, 'Data imported from file appears corrupt or incorrect for this operation.  Please check the import file name.')
if 'policy_list_original' not in export_file_data:
    pc_lib_general.pc_exit_error(404, 'Data imported from file appears corrupt or incorrect for this operation.  Please check the import file name.')
if 'policy_object_original' not in export_file_data:
    pc_lib_general.pc_exit_error(404, 'Data imported from file appears corrupt or incorrect for this operation.  Please check the import file name.')
if 'export_file_version' not in export_file_data:
    pc_lib_general.pc_exit_error(404, 'Data imported from file appears corrupt or incorrect for this operation.  Please check the import file name.')

# The following will check the export version for the correct level.
# If you have an older version that you want to try to import, you can comment out this line,
# but please be aware it will be untested on older versions of an export file.
# At this moment, it *should* still work...
if 'search_object_original' not in export_file_data:
    pc_lib_general.pc_exit_error(404, 'Data imported from file appears corrupt or incorrect for this operation.  Please check the import file name.  Export file may also be an old version.  Please re-export and try again.')
if  export_file_data['export_file_version'] != DEFAULT_COMPLIANCE_IMPORT_FILE_VERSION:
    pc_lib_general.pc_exit_error(404, 'Import file appears to be an unexpected export version.  Please check the import file name.')

# Check the compliance standard and get the JSON information
print('API - Getting the Compliance Standards list...')
pc_settings, response_package = pc_lib_api.api_compliance_standard_list_get(pc_settings)
compliance_standard_list_temp = response_package['data']
compliance_standard_original = export_file_data['compliance_standard_original']
if compliance_standard_original is None:
    pc_lib_general.pc_exit_error(400, 'Compliance Standard not found.  Please check the Compliance Standard name and try again.')
compliance_standard_new_temp = search_list_object_lower(compliance_standard_list_temp, 'name', args.destination_compliance_standard_name)
if compliance_standard_new_temp is not None:
    pc_lib_general.pc_exit_error(400, 'New Compliance Standard appears to already exist.  Please check the new Compliance Standard name and try again.')
print(' Done.')
print()

# Create the new Standard
print('API - Creating the new Compliance Standard...')
compliance_standard_new_temp = {}
compliance_standard_new_temp['name'] = args.destination_compliance_standard_name
if 'description' in compliance_standard_original:
    compliance_standard_new_temp['description'] = compliance_standard_original['description']
pc_settings, response_package = pc_lib_api.api_compliance_standard_add(pc_settings, compliance_standard_new_temp)
compliance_standard_new_response = response_package['data']

# Find the new Standard object
pc_settings, response_package = pc_lib_api.api_compliance_standard_list_get(pc_settings)
compliance_standard_list_temp = response_package['data']
compliance_standard_new = search_list_object(compliance_standard_list_temp, 'name', compliance_standard_new_temp['name'])
if compliance_standard_new is None:
    pc_lib_general.pc_exit_error(500, 'New Compliance Standard was not found!  Sync error?.')
print(' Done.')
print()

# Get the list of requirements that need to be created
print('FILE - Getting Compliance Standard Requirements...')
compliance_requirement_list_original = export_file_data['compliance_requirement_list_original']
print(' Done.')
print()

# Create the new requirements
print('API - Creating the Requirements and adding them to the new Standard...')
for compliance_requirement_original_temp in compliance_requirement_list_original:
    compliance_requirement_new_temp = {}
    compliance_requirement_new_temp['name'] = compliance_requirement_original_temp['name']
    compliance_requirement_new_temp['requirementId'] = compliance_requirement_original_temp['requirementId']
    compliance_requirement_new_temp['viewOrder'] = compliance_requirement_original_temp['viewOrder']
    if 'description' in compliance_requirement_original_temp:
        compliance_requirement_new_temp['description'] = compliance_requirement_original_temp['description']
    pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_add(pc_settings, compliance_standard_new['id'], compliance_requirement_new_temp)
print(' Done.')
print()

# Get new list of requirements
print('API - Getting the new list of requirements...')
pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_list_get(pc_settings, compliance_standard_new['id'])
compliance_requirement_list_new = response_package['data']
print(' Done.')
print()

# Get list of sections and create for each requirement section
print('API - Get list of sections, create them, and associate them to the new requirements (might take a while)...')
# Create mapping list source for policy updates later
map_section_list = []
for compliance_requirement_original_temp in compliance_requirement_list_original:

    # Get sections for requirement
    compliance_section_list_original_temp = export_file_data['compliance_section_list_original'][compliance_requirement_original_temp['id']]

    # Find new ID for requirement
    compliance_requirement_new_temp = search_list_object(compliance_requirement_list_new, 'name', compliance_requirement_original_temp['name'])

    # Create new sections under new ID
    for compliance_section_original_temp in compliance_section_list_original_temp:
        compliance_section_new_temp = {}
        compliance_section_new_temp['sectionId'] = compliance_section_original_temp['sectionId']
        compliance_section_new_temp['viewOrder'] = compliance_section_original_temp['viewOrder']
        if 'description' in compliance_section_original_temp:
            compliance_section_new_temp['description'] = compliance_section_original_temp['description']
        
        pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_section_add(pc_settings, compliance_requirement_new_temp['id'], compliance_section_new_temp)

        # Add entry for mapping table for Policy updates later
        compliance_section_new_temp['requirementGUIDOriginal'] = compliance_requirement_original_temp['id']
        compliance_section_new_temp['requirementGUIDNew'] = compliance_requirement_new_temp['id']
        compliance_section_new_temp['sectionGUIDOriginal'] = compliance_section_original_temp['id']
        compliance_section_new_temp['sectionGUIDNew'] = None
        map_section_list.append(compliance_section_new_temp)
print(' Done.')
print()

########################
## Policy Updates ##

# Check to see if the user wants to try to update the policies
if not args.policy:
    print('Policy switch not specified.  Skipping policy update/attach.  Compliance framework import complete.')
else:
    policy_id_map=json.load(open('PolicyIdMap.json','r'))
    print('Compliance framework import complete.  Policy switch detected.  Starting policy mapping for new compliance framework.')
    print()
    # Need to add the new GUID from the new sections to the mapping tables
    print('API - Getting the new section IDs for the policy mapping and creating a map table...')
    # Timer to make sure everything is posted
    time.sleep(WAIT_TIMER)
    for compliance_requirement_new_temp in compliance_requirement_list_new:

        # Get new sections for requirement
        pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_section_list_get(pc_settings, compliance_requirement_new_temp['id'])
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
                pc_lib_general.pc_exit_error(500, 'New Section cannot find related map for Policy updates!  Sync error?.')
    print('Done.')
    print()

    # Get the policy list that will need to be updated from the import file
    print('FILE - Getting the compliance standard policy list to update from file data...')
    policy_list_original_file = export_file_data['policy_list_original']
    ## Filter out any custom compliance policies that were in the export (This tool cannot import custom compliance policy yet)
    policy_list_original_file_new = []
    for policy_list_original_file_temp in policy_list_original_file:
        if policy_list_original_file_temp['policyMode'] == "custom":
             if policy_list_original_file_temp['policyId'] in policy_id_map:
                 old_policy_id=policy_list_original_file_temp['policyId']
                 new_policy_id=policy_id_map[old_policy_id]
                 
                 #Replace old policy id with new in policy object
                 policy_obj_temp=export_file_data['policy_object_original'][old_policy_id]
                 policy_obj_temp['policyId']=new_policy_id
                 for standard in policy_obj_temp['complianceMetadata']:
                     standard['policyId']=new_policy_id
                 export_file_data['policy_object_original'][new_policy_id]=policy_obj_temp
                 del export_file_data['policy_object_original'][old_policy_id]
                 
                 #Replace old policy id with new in policy list
                 policy_list_original_file_temp['policyId']=new_policy_id
                 policy_list_original_file_new.append(policy_list_original_file_temp)
                 print("Found custom policy, updating ID for current tenant.")
             else:
                 print("Custom policy not yet added to this tenant, dropping from import.")
            #print("Found custom Policy: " + policy_list_original_file_temp['name'] + " ... Dropping it from import.")
        else:
            policy_list_original_file_new.append(policy_list_original_file_temp)
    policy_list_original_file = policy_list_original_file_new
   
    ## Filter Done
    print('Done.')
    print()

    # Cross reference this list with the new tenant policy list and rebuild the list with the new tenant info
    print('API - Pulling policy list from new tenant and syncing with the import file data...')
    pc_settings, response_package = pc_lib_api.api_policy_v2_list_get(pc_settings)
    policy_list_full = response_package['data']
    policy_list_original = []
    for policy_list_original_file_temp in policy_list_original_file:
        success_test = False
        for policy_temp in policy_list_full:
            if policy_list_original_file_temp['policyId'] == policy_temp['policyId']:
                policy_list_original.append(policy_temp)
                success_test = True
                break
        if not success_test:
            pc_lib_general.pc_exit_error(500, 'Policy list in new tenant appears to be missing a policy for mapping.  Check for custom policies in import (custom compliance is not yet supported).')
    if len(policy_list_original_file) != len(policy_list_original):
        pc_lib_general.pc_exit_error(500, 'Mapped policy list appears to be missing a mapped policy.  This should not be possibile?')
    print('Done.')
    print()

    # Work though the list of policies to build the update package
    print('API - Individual policy retrieval and update (might take a while)...')
    policy_update_error = False
    policy_update_error_list = []
    for policy_original_temp in policy_list_original:
        # Get the individual policy JSON object
        pc_settings, response_package = pc_lib_api.api_policy_get(pc_settings, policy_original_temp['policyId'])
        policy_specific_temp = response_package['data']
        print()
        # Need to also get the origional policy object to map in the compliance correctly with the new policy list
        policy_specific_temp_file = export_file_data['policy_object_original'][policy_original_temp['policyId']]

        # Add new compliance section(s)
        complianceMetadata_section_list_new_temp_2 = []
        for complianceMetadata_section_temp in policy_specific_temp_file['complianceMetadata']:
            complianceMetadata_section_new_temp = {}
            for map_section_temp in map_section_list:
                if map_section_temp['sectionGUIDOriginal'] == complianceMetadata_section_temp['complianceId']:
                    complianceMetadata_section_new_temp['customAssigned'] = True
                    complianceMetadata_section_new_temp['systemDefault'] = False
                    complianceMetadata_section_new_temp['complianceId'] = map_section_temp['sectionGUIDNew']
                    complianceMetadata_section_list_new_temp_2.append(complianceMetadata_section_new_temp)
                    break
        if len(complianceMetadata_section_list_new_temp_2) == 0:
            pc_lib_general.pc_exit_error(500, 'Cannot find any compliance section matches in a policy - this should not be possible?')

        # Merge the existing and new lists
        policy_specific_temp['complianceMetadata'].extend(complianceMetadata_section_list_new_temp_2)

        # Add a label (optional) for the new compliance report name
        if args.label:
            policy_specific_temp['labels'].append(args.destination_compliance_standard_name)

        # Post the updated policy to the API
        try:
            print('Updating ' + policy_specific_temp['name'])
            pc_settings, response_package = pc_lib_api.api_policy_update(pc_settings, policy_specific_temp['policyId'], policy_specific_temp)
        except requests.exceptions.HTTPError as e:
            policy_update_error = True
            print('Error updating ' + policy_specific_temp['name'])
            policy_update_error_list.append(policy_specific_temp['name'])

    if policy_update_error:
        print()
        print('An error was encountered when trying to update one or more policies.  Below is a list of the policy name(s) that could not be updated.  '
              'Please manually attach these policies to your new compliance standard, if desired.')
        print()
        for policy_update_error_item in policy_update_error_list:
            print(policy_update_error_item)

    print()
    print('**Compliance copy and policy update complete**')
