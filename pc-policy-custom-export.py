from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
from pc_lib_api import pc_api
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

# --Initialize-- #

pc_lib_general.prompt_for_verification_to_continue(args.yes)
pc_settings = pc_lib_general.pc_settings_get(args.username, args.password, args.uiurl, args.config_file)
pc_api.configure(pc_settings['apiBase'], pc_settings['username'], pc_settings['password'])

# --Main-- #

# Policy Custom Export

export_file_data = {}
export_file_data['export_file_version'] = DEFAULT_POLICY_EXPORT_FILE_VERSION
export_file_data['policy_object_original'] = {}
export_file_data['policy_list_original'] = []
export_file_data['search_object_original'] = {}

print('API - Getting the current list of Custom Policies ...', end='')
policy_list_current = pc_lib_api.api_policy_custom_v2_list_get()
export_file_data['policy_list_original'] = policy_list_current
print(' done.')
print()

print('API - Getting the Custom Policies (please wait) ...')
for policy_current in policy_list_current:
    print('Exporting: %s' % policy_current['name'])
    policy = pc_lib_api.api_policy_get(policy_current['policyId'])
    export_file_data['policy_object_original'][policy_current['policyId']] = policy
    if not 'parameters' in policy_current['rule']:
        continue
    if not 'savedSearch' in policy_current['rule']['parameters']:
        continue
    if policy_current['rule']['parameters']['savedSearch'] == 'true':
        if policy_current['rule']['criteria'] not in export_file_data['search_object_original']:
            search_object_original = pc_lib_api.api_saved_search_get(policy_current['rule']['criteria'])
            export_file_data['search_object_original'][policy_current['rule']['criteria']] = search_object_original
print('Done.')
print()

pc_lib_general.pc_file_write_json(args.export_file_name, export_file_data)
print('Custom Policies exported to: %s' % args.export_file_name)
