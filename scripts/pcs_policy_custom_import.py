""" Import Custom Policies """

import json
import time

import requests

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

CUSTOM_POLICY_ID_MAP_FILE = 'PolicyIdMap.json'
DEFAULT_POLICY_IMPORT_FILE_VERSION = 2
WAIT_TIMER = 5

parser = pc_utility.get_arg_parser()
parser.add_argument(
    'import_file_name',
    type=str,
    help='Import file name for Custom Policies.')
parser.add_argument(
    '--maintain_status',
    action='store_true',
    help='(Optional) - Maintain the status of imported Custom Policies. By default, imported Policies will be disabled.')
args = parser.parse_args()

# --Initialize-- #

pc_utility.prompt_for_verification_to_continue(args)
settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

# Custom Policy Import

import_file_data = pc_utility.read_json_file(args.import_file_name)

# Validation
if 'policy_list_original' not in import_file_data:
    pc_utility.error_and_exit(404, 'policy_list_original section not found. Please verify the import file and name.')
if 'policy_object_original' not in import_file_data:
    pc_utility.error_and_exit(404, 'policy_object_original section not found. Please verify the import file and name.')
if 'export_file_version' not in import_file_data:
    pc_utility.error_and_exit(404, 'export_file_version section not found. Please verify the import file and name.')
if 'search_object_original' not in import_file_data:
    pc_utility.error_and_exit(404, 'search_object_original section not found. Please verify the import file and name.')

# The following will check the export version for the correct level.
# If you have an older version that you want to try to import, you can comment out this line,
# but please be aware it will be untested on older versions of an export file.
# At this moment, it *should* still work...
if  import_file_data['export_file_version'] != DEFAULT_POLICY_IMPORT_FILE_VERSION:
    pc_utility.error_and_exit(404, 'Import file appears to be an unexpected export version. Please verify the import file and name.')

policy_object_original = import_file_data['policy_object_original']
search_object_original = import_file_data['search_object_original']

# For duplicate policy name check.
print('API - Getting the current list of Policies ...', end='')
policy_list_current = pc_api.policy_v2_list_read()
print(' done.')
print()

print('API - Importing Custom Policies ...')
try:
    custom_policy_id_map = json.load(open(CUSTOM_POLICY_ID_MAP_FILE, 'r'))
except (ValueError, FileNotFoundError):
    custom_policy_id_map = {}

for policy_id, policy_object in policy_object_original.items():
    duplicate_found = False
    for policy_current in policy_list_current:
        if policy_object['name'].lower() == policy_current['name'].lower():
            duplicate_found = True
            break
    if duplicate_found:
        print('Skipping Duplicate (by name) Policy: %s' % policy_object['name'])
    else:
        if not args.maintain_status:
            policy_object['enabled'] = False
        # Strip out denormalized data not required to import.
        if 'complianceMetadata' in policy_object:
            policy_object['complianceMetadata'] = []
        policy_object.pop('createdBy', None)
        policy_object.pop('createdOn', None)
        policy_object.pop('deleted', None)
        policy_object.pop('lastModifiedBy', None)
        policy_object.pop('lastModifiedOn', None)
        policy_object.pop('policyID', None)
        policy_object.pop('remediable', None)
        policy_object.pop('ruleLastModifiedOn', None)
        if 'savedSearch' in policy_object['rule']['parameters']:
            if policy_object['rule']['parameters']['savedSearch'] == 'true':
                search_id_to_match = policy_object['rule']['criteria']
                for search_object_id, search_object in search_object_original.items():
                    if 'id' in search_object:
                        if search_object['id'] == search_id_to_match:
                            body_data = {'query': search_object['query'], 'saved': False, 'timeRange': {'type':'relative', 'value': {'unit': 'hour', 'amount': 24}}}
                            new_search = pc_api.saved_search_create(search_object['searchType'], body_data)

                            policy_object['rule']['criteria'] = new_search['id']
                            search_object.pop('id', None)
                            search_object['name'] = '%s _Imported_%s' % (policy_object['name'], int(time.time()))
                            if not search_object['description']:
                                search_object['description'] = 'Imported'
                            search_object['saved'] = True
                            # pc_api.saved_search_create(new_search['id'], search_object)
        new_policy_id = None
        if not args.maintain_status:
            policy_object['enabled'] = False
        try:
            print('Importing: %s' % policy_object['name'])
            new_policy = pc_api.policy_create(policy_object)
            new_policy_id = new_policy['policyId']
        except requests.exceptions.HTTPError as ex:
            print('Error importing: %s' + policy_object['name'])
            print('Possibly, the cloud provider for this Policy is not supported in the destination (esp: api.prismacloud.cn).')
        if new_policy_id is not None:
            custom_policy_id_map[policy_id] = new_policy_id
    print('')
json.dump(custom_policy_id_map, open(CUSTOM_POLICY_ID_MAP_FILE, 'w'))
print('Done.')
print()

print('Import Complete.')
