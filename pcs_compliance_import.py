""" Import a specific Compliance Standard """

import json
import os
import time

import requests

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# TODO: Do not update policy.rule.name when policy.systemDefault == True ?

# --Configuration-- #

CUSTOM_POLICY_ID_MAP_FILE = 'PolicyIdMap.json'
DEFAULT_COMPLIANCE_IMPORT_FILE_VERSION = 3
WAIT_TIMER = 5

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--delete_existing',
    action='store_true',
    help='(Optional) - Delete the Compliance Standard, if it exists, before importing.')
parser.add_argument(
    '--policy',
    action='store_true',
    help='(Optional) - Update Policies with the imported Compliance Standard.')
parser.add_argument(
    '--map_custom_policies',
    action='store_true',
    help='(Optional) - Also update Custom Policies with the imported Compliance Standard (requires --policy).')
parser.add_argument(
    '--label',
    action='store_true',
    help='(Optional) - Add a Label (the name of the Compliance Standard) to updated Policies (requires --policy).')
parser.add_argument(
    'import_file_name',
    type=str,
    help='Import file name for the Compliance Standard.')
parser.add_argument(
    'import_compliance_standard_name',
    type=str,
    help='Name of the Compliance Standard to create.')
args = parser.parse_args()

if args.policy:
    if args.map_custom_policies:
        if not os.path.isfile(CUSTOM_POLICY_ID_MAP_FILE):
            pc_utility.error_and_exit(500, 'Custom policy map file does not exist. Please run pc-policy-custom-export.py and then pc-policy-custom-import.py to generate the file.')

# --Initialize-- #

pc_utility.prompt_for_verification_to_continue(args)
settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

# Compliance Import

import_file_data = pc_utility.read_json_file(args.import_file_name)

# Validation
if 'compliance_standard_original' not in import_file_data:
    pc_utility.error_and_exit(404, 'compliance_standard_original section not found. Please verify the import file and name.')
if 'compliance_requirement_list_original' not in import_file_data:
    pc_utility.error_and_exit(404, 'compliance_requirement_list_original section not found. Please verify the import file and name.')
if 'compliance_section_list_original' not in import_file_data:
    pc_utility.error_and_exit(404, 'compliance_section_list_original section not found. Please verify the import file and name.')
if 'policy_list_original' not in import_file_data:
    pc_utility.error_and_exit(404, 'policy_list_original section not found. Please verify the import file and name.')
if 'policy_object_original' not in import_file_data:
    pc_utility.error_and_exit(404, 'policy_object_original section not found. Please verify the import file and name.')
if 'export_file_version' not in import_file_data:
    pc_utility.error_and_exit(404, 'export_file_version section not found. Please verify the import file and name.')
if import_file_data['export_file_version'] != DEFAULT_COMPLIANCE_IMPORT_FILE_VERSION:
    pc_utility.error_and_exit(404, 'The import file appears to be an unexpected export version. Please verify the import file and name.')

# The following will check the export version for the correct level.
# If you have an older version that you want to try to import, you can comment out this line,
# but please be aware it will be untested on older versions of an export file.
# At this moment, it *should* still work...
if 'search_object_original' not in import_file_data:
    pc_utility.error_and_exit(404, 'search_object_original not found. Please verify the import file and name. The import file may also be an old version: please re-export.')

compliance_standard_original = import_file_data['compliance_standard_original']
if compliance_standard_original is None:
    pc_utility.error_and_exit(400, 'Compliance Standard not found in the import file. Please verify the Compliance Standard name.')

print('API - Getting the current list of Compliance Standards ...', end='')
compliance_standard_list_current = pc_api.compliance_standard_list_read()
compliance_standard = pc_utility.search_list_object_lower(compliance_standard_list_current, 'name', args.import_compliance_standard_name)
print(' done.')
print()

if compliance_standard:
    if args.delete_existing:
        print('API - Deleting the existing Compliance Standard ...', end='')
        pc_api.compliance_standard_delete(compliance_standard['id'])
        print(' done.')
        print()
    else:
        pc_utility.error_and_exit(400, 'Compliance Standard already exists. Please verify the new Compliance Standard name, or delete the existing Compliance Standard.')

print('API - Creating the Compliance Standard ...', end='')
compliance_standard_temp = {}
compliance_standard_temp['name'] = args.import_compliance_standard_name
if 'description' in compliance_standard_original:
    compliance_standard_temp['description'] = compliance_standard_original['description']
pc_api.compliance_standard_create(compliance_standard_temp)
print(' done.')
print()

print('API - Getting the newly created Compliance Standard ...', end='')
time.sleep(WAIT_TIMER)
compliance_standard_list_current = pc_api.compliance_standard_list_read()
compliance_standard_new = pc_utility.search_list_object(compliance_standard_list_current, 'name', compliance_standard_temp['name'])
if compliance_standard_new is None:
    pc_utility.error_and_exit(500, 'New Compliance Standard not found.')
print(' done.')
print()

print('API - Creating the Requirements and adding them to the new Compliance Standard ...', end='')
compliance_requirement_list_original = import_file_data['compliance_requirement_list_original']
for compliance_requirement_original in compliance_requirement_list_original:
    compliance_requirement_temp = {}
    compliance_requirement_temp['name']          = compliance_requirement_original['name']
    compliance_requirement_temp['requirementId'] = compliance_requirement_original['requirementId']
    compliance_requirement_temp['viewOrder']     = compliance_requirement_original['viewOrder']
    if 'description' in compliance_requirement_original:
        compliance_requirement_temp['description'] = compliance_requirement_original['description']
    pc_api.compliance_standard_requirement_create(compliance_standard_new['id'], compliance_requirement_temp)
print(' done.')
print()

print('API - Getting the newly created Compliance Standard Requirements ...', end='')
time.sleep(WAIT_TIMER)
compliance_requirement_list_new = pc_api.compliance_standard_requirement_list_read(compliance_standard_new['id'])
print(' done.')
print()

print('API - Creating the Sections and adding them to the new Requirements ...', end='')
sections_to_map_to_policies = []
for compliance_requirement_original in compliance_requirement_list_original:
    compliance_section_list_original = import_file_data['compliance_section_list_original'][compliance_requirement_original['id']]
    compliance_requirement_temp = pc_utility.search_list_object(compliance_requirement_list_new, 'name', compliance_requirement_original['name'])
    for compliance_section_original in compliance_section_list_original:
        compliance_section_temp = {}
        compliance_section_temp['sectionId'] = compliance_section_original['sectionId']
        compliance_section_temp['viewOrder'] = compliance_section_original['viewOrder']
        if 'description' in compliance_section_original:
            compliance_section_temp['description'] = compliance_section_original['description']
        pc_api.compliance_standard_requirement_section_create(compliance_requirement_temp['id'], compliance_section_temp)
        # Mapping Sections to Policies
        compliance_section_temp['original_compliance_requirement_id'] = compliance_requirement_original['id']
        compliance_section_temp['original_compliance_section_id']     = compliance_section_original['id']
        compliance_section_temp['new_compliance_requirement_id']      = compliance_requirement_temp['id']
        compliance_section_temp['new_compliance_section_id']          = None
        sections_to_map_to_policies.append(compliance_section_temp)
print(' done.')
print()

# TODO: Save state here, to allow restarting from here.
# TODO: Add Object counts as a progress bar.

## Policy Mapping ##

if args.policy:
    if args.map_custom_policies:
        custom_policy_id_map = json.load(open(CUSTOM_POLICY_ID_MAP_FILE, 'r'))
    else:
        custom_policy_id_map = []
    print('Mapping Policies to the new Compliance Standard.')
    print()
    print('API - Validating the newly created Compliance Standard Requirement Sections ...', end='')
    time.sleep(WAIT_TIMER)
    # TODO: Replace inner and outer looping.
    for compliance_requirement_new in compliance_requirement_list_new:
        # Get the new Sections for the new Requirement.
        compliance_section_list_new = pc_api.compliance_standard_requirement_section_list_read(compliance_requirement_new['id'])
        # Get the new IDs for the new Sections.
        for compliance_section_new in compliance_section_list_new:
            found = False
            for section_to_map in sections_to_map_to_policies:
                if section_to_map['new_compliance_requirement_id'] == compliance_requirement_new['id'] and section_to_map['sectionId'] == compliance_section_new['sectionId']:
                    section_to_map['new_compliance_section_id'] = compliance_section_new['id']
                    found = True
                    break
            if not found:
                pc_utility.error_and_exit(500, 'Failed to validate the new Section: %s for Requirement: %s' % (compliance_section_new['id'], compliance_requirement_new['id']))
    print(' done.')
    print()

    policy_list_original = import_file_data['policy_list_original']
    policy_list_updated = []
    for policy in policy_list_original:
        if policy['policyMode'] == 'custom':
            if policy['policyId'] in custom_policy_id_map:
                old_policy_id = policy['policyId']
                new_policy_id = custom_policy_id_map[old_policy_id]
                # Replace old Policy ID with new Policy ID in Policy object.
                policy_object_original = import_file_data['policy_object_original'][old_policy_id]
                policy_object_original['policyId'] = new_policy_id
                for standard in policy_object_original['complianceMetadata']:
                    standard['policyId'] = new_policy_id
                import_file_data['policy_object_original'][new_policy_id] = policy_object_original
                del import_file_data['policy_object_original'][old_policy_id]
                # Replace old Policy ID with new Policy ID in the updated Policy list.
                policy['policyId'] = new_policy_id
                policy_list_updated.append(policy)
                # print('Found Custom Policy in destination, updating ID from: %s to %s for %s' % (old_policy_id, new_policy_id, policy['name']))
            else:
                pass
        else:
            policy_list_updated.append(policy)

    # Compare updated (policyId) Policies with current Policies, and build a list of validated Policies.
    print('API - Getting the current list of Policies ...', end='')
    policy_list_current = pc_api.policy_v2_list_read()
    policy_validate_error_list = []
    policy_list_updated_validated = []
    # TODO: Replace inner and outer looping.
    for policy_updated in policy_list_updated:
        found = False
        for policy_current in policy_list_current:
            if policy_updated['policyId'] == policy_current['policyId']:
                policy_list_updated_validated.append(policy_current)
                found = True
                break
        if not found:
            if 'cloudType' in policy_updated:
                item = '%s %s %s' % (policy_updated['policyId'], policy_updated['cloudType'], policy_updated['name'])
            else:
                item = '%s %s' % (policy_updated['policyId'], policy_updated['name'])
            policy_validate_error_list.append(item)
    print(' done.')
    print()

    # TODO: Use error logging as per pc-resources-export.py.
    if policy_validate_error_list:
        print()
        print('The following is a list of the Policies that could not be found in the destination.')
        print('Possibly, the cloud provider for these Policies are not supported in the destination (esp: api.prismacloud.cn).')
        print()
        for policy_validate_error in policy_validate_error_list:
            print(policy_validate_error)
        print()

    # Work though the list of Policies to update.
    print('API - Getting and updating the Policy list (please wait) ...')
    policy_update_error_list = []
    for policy_updated_validated in policy_list_updated_validated:
        policy_current = pc_api.policy_read(policy_updated_validated['policyId'])
        policy_object_original = import_file_data['policy_object_original'][policy_updated_validated['policyId']]
        # Add new Compliance Standard Section(s).
        compliance_metadata_to_merge = []
        for compliance_metadata_original in policy_object_original['complianceMetadata']:
            compliance_metadata_updated = {}
            for section_to_map in sections_to_map_to_policies:
                if section_to_map['original_compliance_section_id'] == compliance_metadata_original['complianceId']:
                    # compliance_metadata_updated['standardName']    =
                    # compliance_metadata_updated['requirementName'] =
                    compliance_metadata_updated['complianceId']    = section_to_map['new_compliance_section_id']
                    # compliance_metadata_updated['requirementId']   =
                    # compliance_metadata_updated['sectionId']       =
                    compliance_metadata_updated['customAssigned']  = True
                    compliance_metadata_updated['systemDefault']   = False
                    compliance_metadata_to_merge.append(compliance_metadata_updated)
                    break
        if len(compliance_metadata_to_merge) == 0:
            pc_utility.error_and_exit(500, 'Cannot find any Compliance metadata for Policy object %s' % policy_updated_validated['policyId'])
        policy_current['complianceMetadata'].extend(compliance_metadata_to_merge)
        if args.label:
            policy_current['labels'].append(args.import_compliance_standard_name)
        try:
            print('Updating Policy: %s' % policy_current['name'])
            pc_api.policy_update(policy_current['policyId'], policy_current)
        except requests.exceptions.HTTPError as ex:
            policy_update_error_list.append(policy_current['name'])
            print('Error updating Policy: %s\n\t%s' % (policy_current['name'], ex))
    if policy_update_error_list:
        print()
        print('The following is a list of the Policies that could not be updated.')
        print('Please map those Policies to the new Compliance Standard in the Console.')
        print()
        for policy_update_error in policy_update_error_list:
            print(policy_update_error)
        print()
    print('Done.')
    print()

print('Import Complete.')
