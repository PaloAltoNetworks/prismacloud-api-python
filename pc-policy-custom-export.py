from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import pc_lib_api
import pc_lib_general

# --Configuration-- #

DEFAULT_POLICY_EXPORT_FILE_VERSION = 2

parser = pc_lib_general.pc_arg_parser_defaults()
parser.add_argument(
    'export_file_name',
    type=str,
    help='Export file name for the Custom Policies.')
args = parser.parse_args()

# --Main-- #

pc_lib_general.prompt_for_verification_to_continue(args.yes)

print('API - Getting login ...', end='')
pc_settings = pc_lib_general.pc_login_get(args.username, args.password, args.uiurl, args.config_file)
pc_settings = pc_lib_api.pc_jwt_get(pc_settings)
print(' done.')
print()

## Policy Export ##

export_file_data = {}
export_file_data['export_file_version'] = DEFAULT_POLICY_EXPORT_FILE_VERSION
export_file_data['policy_object_original'] = {}
export_file_data['policy_list_original'] = []
export_file_data['search_object_original'] = {}

print('API - Getting the current list of Custom Policies ...', end='')
pc_settings, response_package = pc_lib_api.api_policy_custom_v2_list_get(pc_settings)
policy_list_original = response_package['data']
export_file_data['policy_list_original'] = policy_list_original
print(' done.')
print()

print('API - Getting the Custom Policies (please wait) ...')
for policy_original in policy_list_original:
    print('Exporting: %s' % policy_original['name'])
    pc_settings, response_package = pc_lib_api.api_policy_get(pc_settings, policy_original['policyId'])
    policy = response_package['data']
    export_file_data['policy_object_original'][policy_original['policyId']] = policy
    if 'savedSearch' in policy_original['rule']['parameters']:
        if policy_original['rule']['parameters']['savedSearch'] == 'true':
            if policy_original['rule']['criteria'] not in export_file_data['search_object_original']:
                pc_settings, response_package = pc_lib_api.api_search_get(pc_settings, policy_original['rule']['criteria'])
                search_object_original = response_package['data']
                export_file_data['search_object_original'][policy_original['rule']['criteria']] = search_object_original
print('Done.')
print()

pc_lib_general.pc_file_write_json(args.export_file_name, export_file_data)
print('Custom Policies exported to: %s' % args.export_file_name)
print()
