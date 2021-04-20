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

parser = pc_lib_general.pc_arg_parser_defaults()
parser.add_argument(
    '-policy',
    '--policy',
    action='store_true',
    help='(Optional) - If you want to update policies with the imported compliance standard, add this switch to the command.')
parser.add_argument(
    '--map_custom_policies',
    action='store_true',
    help='(Optional) - If you want to update custom policies with the imported compliance standard, add this switch to the command.')
parser.add_argument(
    '-label',
    '--label',
    action='store_true',
    help='(Optional) - Add a label to any policy updated with the imported compliance standard. Requires the --policy switch.')
parser.add_argument(
    'source_import_file_name',
    type=str,
    help='Name of the compliance standard import file.')
parser.add_argument(
    'destination_compliance_standard_name',
    type=str,
    help='Name of the new compliance standard to create.')
args = parser.parse_args()

# --Main-- #

pc_settings = pc_lib_general.pc_login_get(args.username, args.password, args.uiurl, args.config_file)

# Verification (override with -y)
if not args.yes:
    print()
    print('Ready to execute commands against your Prisma Cloud tenant.')
    verification_response = str(input('Would you like to continue (y or yes to continue)?'))
    continue_response = {'yes', 'y'}
    print()
    if verification_response not in continue_response:
        pc_lib_general.pc_exit_error(400, 'Verification failed due to user response. Exiting...')

if args.policy:
    if args.map_custom_policies:
        if not os.path.isfile('PolicyIdMap.json'):
            pc_lib_general.pc_exit_error(500, 'PolicyIdMap.json does not exist. Run pc-policy-custom-export.py and then pc-policy-custom-import.py')

# Sort out API Login
print('API - Getting authentication token...')
pc_settings = pc_lib_api.pc_jwt_get(pc_settings)
print(' Done.')
print()

## Compliance Import ##

import_file_data = pc_lib_general.pc_file_read_json(args.source_import_file_name)

# Validation
if 'compliance_standard_original' not in import_file_data:
    pc_lib_general.pc_exit_error(404, 'compliance_standard_original section not found. Please check the import file and name.')
if 'compliance_requirement_list_original' not in import_file_data:
    pc_lib_general.pc_exit_error(404, 'compliance_requirement_list_original section not found. Please check the import file and name.')
if 'compliance_section_list_original' not in import_file_data:
    pc_lib_general.pc_exit_error(404, 'compliance_section_list_original section not found. Please check the import file and name.')
if 'policy_list_original' not in import_file_data:
    pc_lib_general.pc_exit_error(404, 'policy_list_original section not found. Please check the import file and name.')
if 'policy_object_original' not in import_file_data:
    pc_lib_general.pc_exit_error(404, 'policy_object_original section not found. Please check the import file and name.')
if 'export_file_version' not in import_file_data:
    pc_lib_general.pc_exit_error(404, 'export_file_version section not found. Please check the import file and name.')
if import_file_data['export_file_version'] != DEFAULT_COMPLIANCE_IMPORT_FILE_VERSION:
    pc_lib_general.pc_exit_error(404, 'The import file appears to be an unexpected export version. Please check the import file and name.')

# The following will check the export version for the correct level.
# If you have an older version that you want to try to import, you can comment out this line,
# but please be aware it will be untested on older versions of an export file.
# At this moment, it *should* still work...
if 'search_object_original' not in import_file_data:
    pc_lib_general.pc_exit_error(404, 'search_object_original not found. Please check the import file and name. The import file may also be an old version: please re-export and try again.')

compliance_standard_original = import_file_data['compliance_standard_original']
if compliance_standard_original is None:
    pc_lib_general.pc_exit_error(400, 'Compliance Standard not found in the import file. Please check the Compliance Standard name and try again.')

print('API - Getting the current list of Compliance Standards ...')
pc_settings, response_package = pc_lib_api.api_compliance_standard_list_get(pc_settings)
compliance_standard_list_current = response_package['data']
compliance_standard = search_list_object_lower(compliance_standard_list_current, 'name', args.destination_compliance_standard_name)
if compliance_standard is not None:
    pc_lib_general.pc_exit_error(400, 'Compliance Standard already exists. Please check the new Compliance Standard name and try again.')
print(' Done.')
print()

# pc_lib_general.pc_exit_error(500, 'EXIT')

print('API - Creating the new Compliance Standard ...')
compliance_standard_temp = {}
compliance_standard_temp['name'] = args.destination_compliance_standard_name
if 'description' in compliance_standard_original:
    compliance_standard_temp['description'] = compliance_standard_original['description']
pc_settings, response_package = pc_lib_api.api_compliance_standard_add(pc_settings, compliance_standard_temp)
print(' Done.')
print()

print('API - Getting the newly created Compliance Standard ...')
time.sleep(WAIT_TIMER)
pc_settings, response_package = pc_lib_api.api_compliance_standard_list_get(pc_settings)
compliance_standard_list_current = response_package['data']
compliance_standard_new = search_list_object(compliance_standard_list_current, 'name', compliance_standard_temp['name'])
if compliance_standard_new is None:
    pc_lib_general.pc_exit_error(500, 'New Compliance Standard not found! Sync error?.')
print(' Done.')
print()

print('API - Creating the Requirements and adding them to the new Compliance Standard ...')
compliance_requirement_list_original = import_file_data['compliance_requirement_list_original']
for compliance_requirement_original in compliance_requirement_list_original:
    compliance_requirement_temp = {}
    compliance_requirement_temp['name']          = compliance_requirement_original['name']
    compliance_requirement_temp['requirementId'] = compliance_requirement_original['requirementId']
    compliance_requirement_temp['viewOrder']     = compliance_requirement_original['viewOrder']
    if 'description' in compliance_requirement_original:
        compliance_requirement_temp['description'] = compliance_requirement_original['description']
    pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_add(pc_settings, compliance_standard_new['id'], compliance_requirement_temp)
print(' Done.')
print()

print('API - Getting the newly created Compliance Standard Requirements ...')
time.sleep(WAIT_TIMER)
pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_list_get(pc_settings, compliance_standard_new['id'])
compliance_requirement_list_new = response_package['data']
print(' Done.')
print()

print('API - Creating the Sections and adding them to the new Requirements (please wait) ...')
sections_to_map_to_policies = []
for compliance_requirement_original in compliance_requirement_list_original:
    compliance_section_list_original = import_file_data['compliance_section_list_original'][compliance_requirement_original['id']]
    compliance_requirement_temp = search_list_object(compliance_requirement_list_new, 'name', compliance_requirement_original['name'])
    for compliance_section_original in compliance_section_list_original:
        compliance_section_temp = {}
        compliance_section_temp['sectionId'] = compliance_section_original['sectionId']
        compliance_section_temp['viewOrder'] = compliance_section_original['viewOrder']
        if 'description' in compliance_section_original:
            compliance_section_temp['description'] = compliance_section_original['description']
        pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_section_add(pc_settings, compliance_requirement_temp['id'], compliance_section_temp)
        # Mapping Sections to Policies
        compliance_section_temp['original_compliance_requirement_id'] = compliance_requirement_original['id']
        compliance_section_temp['original_compliance_section_id']     = compliance_section_original['id']
        compliance_section_temp['new_compliance_requirement_id']      = compliance_requirement_temp['id']
        compliance_section_temp['new_compliance_section_id']          = None
        sections_to_map_to_policies.append(compliance_section_temp)
print(' Done.')
print()

print('Compliance Standard Imported.')
print()

# TODO: Save state here, to allow restarting from here.

## Policy Mapping ##

if args.policy:
    if args.map_custom_policies:
        print('Mapping Policies to the new Compliance Standard.')
        print()
        policy_id_map = json.load(open('PolicyIdMap.json', 'r'))
        print('API - Validating the newly created Compliance Standard Requirement Sections ...')
        time.sleep(WAIT_TIMER)
        # TODO: Replace double loop.
        for compliance_requirement_new in compliance_requirement_list_new:
            # Get the new Sections for the new Requirement.
            pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_section_list_get(pc_settings, compliance_requirement_new['id'])
            compliance_section_list_new = response_package['data']
            # Get the new IDs for the new Sections and update the section_to_map (or sections_to_map_to_policies ?).
            for compliance_section_new in compliance_section_list_new:
                mapped = False
                for section_to_map in sections_to_map_to_policies:
                    if section_to_map['new_compliance_requirement_id'] == compliance_requirement_new['id'] and section_to_map['sectionId'] == compliance_section_new['sectionId']:
                        section_to_map['new_compliance_section_id'] = compliance_section_new['id']
                        mapped = True
                        break
                if not mapped:
                    pc_lib_general.pc_exit_error(500, 'Failed to validate the new Section: %s ' % (section_to_map))
        print(' Done.')
        print()
    else:
        policy_id_map = []

    policy_list_original = import_file_data['policy_list_original']
    policy_list_updated = []
    for policy in policy_list_original:
        if policy['policyMode'] == 'custom':
            if policy['policyId'] in policy_id_map:
                old_policy_id = policy['policyId']
                new_policy_id = policy_id_map[old_policy_id]
                # Replace old Policy ID with new Policy ID in Policy object.
                policy_object_original = import_file_data['policy_object_original'][old_policy_id]
                policy_object_original['policyId'] = new_policy_id
                for standard in policy_object_original['complianceMetadata']:
                    standard['policyId'] = new_policy_id
                import_file_data['policy_object_original'][new_policy_id] = policy_object_original
                del import_file_data['policy_object_original'][old_policy_id]
                # Replace old Policy ID with new Policy ID in updated Policy list.
                policy['policyId'] = new_policy_id
                policy_list_updated.append(policy)
                # print('Found custom policy, updating ID for current tenant.)
            else:
                pass
                # print('Custom policy not yet added to this tenant, dropping from import.')
        else:
            policy_list_updated.append(policy)

    # Cross-reference policy_list_updated with policy_list_current, and build policy_list_updated_validated.
    print('API - Getting the Policy list ...')
    pc_settings, response_package = pc_lib_api.api_policy_v2_list_get(pc_settings)
    policy_list_current = response_package['data']
    policy_list_updated_validated = []
    for policy_updated in policy_list_updated:
        found = False
        for policy_current in policy_list_current:
            if policy_updated['policyId'] == policy_current['policyId']:
                policy_list_updated_validated.append(policy_current)
                found = True
                break
        if not found:
            pc_lib_general.pc_exit_error(500, 'Current Policy list appears to be missing a Policy for mapping.')
    if len(policy_list_updated) != len(policy_list_updated_validated):
        pc_lib_general.pc_exit_error(500, 'Mapped Policy list appears to be missing a mapped Policy.')
    print('Done.')
    print()

    # Work though the list of policies to build an update.
    print('API - Getting and updating the Policy list (please wait) ...')
    policy_update_error = False
    policy_update_error_list = []
    for policy_updated_validated in policy_list_updated_validated:
        pc_settings, response_package = pc_lib_api.api_policy_get(pc_settings, policy_updated_validated['policyId'])
        policy_current = response_package['data']
        policy_object_original = import_file_data['policy_object_original'][policy_updated_validated['policyId']]
        # Add new Compliance Standard Section(s).
        compliance_metadata_to_merge = []
        for compliance_metadata_original in policy_object_original['complianceMetadata']:
            compliance_metadata_updated = {}
            for section_to_map in sections_to_map_to_policies:
                if section_to_map['original_compliance_section_id'] == compliance_metadata_original['complianceId']:
                    compliance_metadata_updated['systemDefault']  = False
                    compliance_metadata_updated['customAssigned'] = True
                    compliance_metadata_updated['complianceId']   = section_to_map['new_compliance_section_id']
                    compliance_metadata_to_merge.append(compliance_metadata_updated)
                    break
        if len(compliance_metadata_to_merge) == 0:
            pc_lib_general.pc_exit_error(500, 'Cannot find any Compliance metadata for Policy object %s' % compliance_metadata_original)

        # Merge the existing and new lists
        policy_current['complianceMetadata'].extend(compliance_metadata_to_merge)

        # Add a label (optional) for the new compliance report name
        if args.label:
            policy_current['labels'].append(args.destination_compliance_standard_name)

        # Post the updated policy to the API
        try:
            print('Updating %s' % policy_current['name'])
            pc_settings, response_package = pc_lib_api.api_policy_update(pc_settings, policy_current['policyId'], policy_current)
        except requests.exceptions.HTTPError as e:
            policy_update_error = True
            print('Error updating %s' % policy_current['name'])
            policy_update_error_list.append(policy_current['name'])

    if policy_update_error:
        print()
        print('An error was encountered when trying to update one or more policies.')
        print('Below is a list of the policies that could not be updated.')
        print('Please manually map those policies to the new Compliance Standard, if desired.')
        print()
        for policy_update_error in policy_update_error_list:
            print(policy_update_error)
    print()
    print('Policies mapped to the new Compliance Standard.')
