from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import pc_lib_api
import pc_lib_general
import json
import random
import requests
import time

# --Configuration-- #

CUSTOM_POLICY_ID_MAP_FILE = 'PolicyIdMap.json'
DEFAULT_POLICY_IMPORT_FILE_VERSION = 2
WAIT_TIMER = 5

parser = pc_lib_general.pc_arg_parser_defaults()
parser.add_argument(
    'import_file_name',
    type=str,
    help='Import file name for Custom Policies.')
parser.add_argument(
    '--status',
    action='store_true',
    help='(Optional) - Maintain the status of imported Custom Policies. By default, they will be disabled.')
args = parser.parse_args()

# --Main-- #

pc_lib_general.prompt_for_verification_to_continue(args.yes)

print('API - Getting login ...', end='')
pc_settings = pc_lib_general.pc_login_get(args.username, args.password, args.uiurl, args.config_file)
pc_settings = pc_lib_api.pc_jwt_get(pc_settings)
print(' done.')
print()

# Custom Policy Import

import_file_data = pc_lib_general.pc_file_read_json(args.import_file_name)

# Validation
if 'policy_list_original' not in import_file_data:
    pc_lib_general.pc_exit_error(404, 'policy_list_original section not found. Please verify the import file and name.')
if 'policy_object_original' not in import_file_data:
    pc_lib_general.pc_exit_error(404, 'policy_object_original section not found. Please verify the import file and name.')
if 'export_file_version' not in import_file_data:
    pc_lib_general.pc_exit_error(404, 'export_file_version section not found. Please verify the import file and name.')
if 'search_object_original' not in import_file_data:
    pc_lib_general.pc_exit_error(404, 'search_object_original section not found. Please verify the import file and name.')

# The following will check the export version for the correct level.
# If you have an older version that you want to try to import, you can comment out this line,
# but please be aware it will be untested on older versions of an export file.
# At this moment, it *should* still work...
if  import_file_data['export_file_version'] != DEFAULT_POLICY_IMPORT_FILE_VERSION:
    pc_lib_general.pc_exit_error(404, 'Import file appears to be an unexpected export version. Please verify the import file and name.')

policy_object_original = import_file_data['policy_object_original']
search_object_original = import_file_data['search_object_original']

# For duplicate policy name check.
print('API - Getting the current list of Policies ...', end='')
pc_settings, response_package = pc_lib_api.api_policy_v2_list_get(pc_settings)
policy_list_current = response_package['data']
print(' done.')
print()

print('API - Importing Custom Policies ...')
try:
    custom_policy_id_map = json.load(open(CUSTOM_POLICY_ID_MAP_FILE, 'r'))
except:
    custom_policy_id_map = {}

for policy_id, policy_object in policy_object_original.items():
    duplicate_found = False
    for policy_current in policy_list_current:
        if policy_object['name'].lower() == policy_current['name'].lower():
            duplicate_found = True
            break
    if duplicate_found:
        print('Skipping Duplicate (by name) Policy: %' % policy_object['name'])
    else:
        if not args.status:
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
                            pc_settings, response_package = pc_lib_api.api_search_add(pc_settings, search_object['searchType'], body_data)
                            new_search = response_package['data']
                            policy_object['rule']['criteria'] = new_search['id']
                            search_object.pop('id', None)
                            # TODO: Validate need for timestamp and random string:
                            # alph = [i for i in 'abcdefghijklmnopqrstuvwxyz0123456789']
                            # ''.join([random.choice(alph) for _ in range(4)])
                            search_object['name'] = '%s _Imported_%s' % (policy_object['name'], int(time.time()))
                            if not search_object['description']:
                                search_object['description'] = 'Imported'
                            search_object['saved'] = True
                            pc_settings, response_package = pc_lib_api.api_saved_search_add(pc_settings, new_search['id'], search_object)
        new_policy_id = None
        if not args.status:
            policy_object['enabled'] = False
        try:
            print('Importing: %s' % policy_object['name'])
            pc_settings, response_package = pc_lib_api.api_policy_add(pc_settings, policy_object)
            new_policy_id = response_package['data']['policyId']
        except requests.exceptions.HTTPError as e:
            print('Error importing: %s' + policy_object['name'])
            print('Possibly, the cloud provider for this Policy is not supported in the destination (esp: api.prismacloud.cn).')
        if new_policy_id is not None:
            custom_policy_id_map[policy_id] = new_policy_id
    print('')
json.dump(custom_policy_id_map, open(CUSTOM_POLICY_ID_MAP_FILE, 'w'))
print('Done.')
print()

print('Import Complete.')
