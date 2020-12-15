from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import pc_lib_api
import pc_lib_general
import time
import requests
import random
import time

alph=[i for i in 'abcdefghijklmnopqrstuvwxyz0123456789']

# --Configuration-- #
# Import file version expected
DEFAULT_POLICY_IMPORT_FILE_VERSION = 2
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
    'source_import_file_name',
    type=str,
    help='Name of the file to import the new compliance standard from.')

parser.add_argument(
    '-status',
    '--status',
    action='store_true',
    help='(Optional) - Custom policies will import with a disabled status by default.  If you would like to maintain whatever status was exported, include this switch.')

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

# Read in the JSON import file
export_file_data = pc_lib_general.pc_file_read_json(args.source_import_file_name)

# Do a quick validation to see if we are getting the base keys
if 'policy_list_original' not in export_file_data:
    pc_lib_general.pc_exit_error(404, 'Data imported from file appears corrupt or incorrect for this operation.  Please check the import file name.')
if 'policy_object_original' not in export_file_data:
    pc_lib_general.pc_exit_error(404, 'Data imported from file appears corrupt or incorrect for this operation.  Please check the import file name.')
if 'export_file_version' not in export_file_data:
    pc_lib_general.pc_exit_error(404, 'Data imported from file appears corrupt or incorrect for this operation.  Please check the import file name.')
if 'search_object_original' not in export_file_data:
    pc_lib_general.pc_exit_error(404, 'Data imported from file appears corrupt or incorrect for this operation.  You may be using an older export format that this tool cannot support.  Please re-export with the latest tools.')

# The following will check the export version for the correct level.
# If you have an older version that you want to try to import, you can comment out this line,
# but please be aware it will be untested on older versions of an export file.
# At this moment, it *should* still work...
if  export_file_data['export_file_version'] != DEFAULT_POLICY_IMPORT_FILE_VERSION:
    pc_lib_general.pc_exit_error(404, 'Import file appears to be an unexpected export version.  Please check the import file name.')

# Get the policies and related searches that will need to be imported from the import file
print('FILE - Getting the policy list to import from file data...')
policy_object_original_file = export_file_data['policy_object_original']
search_object_original_file = export_file_data['search_object_original']
print('Done.')
print()

# Get the policy list from the tenant for duplicate name check
print('API - Pulling policy list from new tenant...')
pc_settings, response_package = pc_lib_api.api_policy_v2_list_get(pc_settings)
policy_list_full = response_package['data']
print('Done.')
print()
##print(json.dumps(policy_object_original_file))
# Import the custom policies

policy_mapping_dict={}
try:
    policy_mapping_dict=json.load(open('PolicyIdMap.json','r'))
except:
    pass
for policy_id_temp,policy_object_original_file_temp in policy_object_original_file.items():
    # Check to see if there is already a policy with the same name
    
    duplicate_name=False
    for policy_temp in policy_list_full:
        if policy_object_original_file_temp['name'].lower() == policy_temp['name'].lower():
            duplicate_name = True
            break
    if duplicate_name:
        print('Tenant appears to already have a policy by the name of: ' +  policy_object_original_file_temp['name'] + '.  Skipping import for this policy...')
    else:
        config_search=True

        # Strip out Complaince connections and related fields that are not needed for import
        if 'complianceMetadata' in policy_object_original_file_temp:
            policy_object_original_file_temp['complianceMetadata'] = []
        policy_object_original_file_temp.pop('policyID', None)
        if not args.status:
            policy_object_original_file_temp['enabled'] = False
        policy_object_original_file_temp.pop('createdOn', None)
        policy_object_original_file_temp.pop('createdBy', None)
        policy_object_original_file_temp.pop('lastModifiedOn', None)
        policy_object_original_file_temp.pop('lastModifiedBy', None)
        policy_object_original_file_temp.pop('ruleLastModifiedOn', None)
        policy_object_original_file_temp.pop('deleted', None)
        policy_object_original_file_temp.pop('remediable', None)
##########################################################
        # Import saved search (if required)
        if 'savedSearch' in policy_object_original_file_temp['rule']['parameters']:
            if policy_object_original_file_temp['rule']['parameters']['savedSearch'] == "true":
                id_to_match=policy_object_original_file_temp['rule']['criteria']
                for search_object_id_temp,search_object_original_file_temp in search_object_original_file.items():
                    if 'id' in search_object_original_file_temp:
                        if search_object_original_file_temp['id'] == id_to_match:
                            search=search_object_original_file_temp
                            query=search['query']
                            search_type=search['searchType']
                            body_data={'query':query,'saved':False,'timeRange':{"type":"relative","value":{"unit":"hour","amount":24}}}
                                
                            resp=pc_lib_api.api_search_add(pc_settings, search_type, body_data)
                            
                            new_search_id=resp[1]['data']['id']
                            # Clean up the saved search object for import
                            search.pop('id', None)            
                            search['name']='customSearch'+str(int(time.time()))+''.join([random.choice(alph) for _ in range(5)])
                            search['description'] = 'test Description'
                            search['saved']=True
                             
                                                       
                            pc_lib_api.api_saved_search_add(pc_settings,new_search_id,search)
                            policy_object_original_file_temp['rule']['criteria']=new_search_id
                            print("Finished recreating saved search.")
                           
                            
        
###########################################################
        new_policy_id=None
        # Check to see if the new policies should come in disabled or maintain their exported status
        if args.status:
            # Import with existing status
            try:
                print('Importing ' + policy_object_original_file_temp['name'])
                pc_settings, response_package = pc_lib_api.api_policy_add(pc_settings, policy_object_original_file_temp)
                new_policy_id=response_package['data']['policyId']
            except requests.exceptions.HTTPError as e:
                policy_update_error = True
                print('Error importing ' + policy_object_original_file_temp['name'])
        else:
            # Import with a status of disabled
            policy_object_original_file_temp['enabled'] = False
            try:
                print('Importing ' + policy_object_original_file_temp['name'])
                pc_settings, response_package = pc_lib_api.api_policy_add(pc_settings, policy_object_original_file_temp)
                new_policy_id=response_package['data']['policyId']
            except requests.exceptions.HTTPError as e:
                policy_update_error = True
                print('Error importing ' + policy_object_original_file_temp['name'])
        
        if new_policy_id is not None:
            policy_mapping_dict[policy_id_temp]=new_policy_id
    print('')
json.dump(policy_mapping_dict,open('PolicyIdMap.json','w'))
            
                

print()
print('Import Complete.')
