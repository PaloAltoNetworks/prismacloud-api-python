from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import pc_lib_api
import pc_lib_general

# --Configuration-- #

DEFAULT_COMPLIANCE_EXPORT_FILE_VERSION = 3

parser = pc_lib_general.pc_arg_parser_defaults()
parser.add_argument(
    'source_compliance_standard_name',
    type=str,
    help='Name of the Compliance Standard to export.')
parser.add_argument(
    'export_file_name',
    type=str,
    help='Export file name for the Compliance Standard.')
args = parser.parse_args()

# --Main-- #

pc_lib_general.prompt_for_verification_to_continue(args.yes)

print('API - Getting login ...', end='')
pc_settings = pc_lib_general.pc_login_get(args.username, args.password, args.uiurl, args.config_file)
pc_settings = pc_lib_api.pc_jwt_get(pc_settings)
print(' done.')
print()

## Compliance Export ##

export_file_data = {}
export_file_data['export_file_version'] = DEFAULT_COMPLIANCE_EXPORT_FILE_VERSION
export_file_data['compliance_section_list_original'] = {}
export_file_data['policy_object_original'] = {}
export_file_data['policy_list_original'] = []
export_file_data['search_object_original'] = {}

print('API - Getting the current list of Compliance Standards ...', end='')
pc_settings, response_package = pc_lib_api.api_compliance_standard_list_get(pc_settings)
compliance_standard_list_current = response_package['data']
compliance_standard_original = pc_lib_general.search_list_object_lower(compliance_standard_list_current, 'name', args.source_compliance_standard_name)
if compliance_standard_original is None:
    pc_lib_general.pc_exit_error(400, 'Compliance Standard to export not found. Please verify the Compliance Standard name.')
export_file_data['compliance_standard_original'] = compliance_standard_original
print(' done.')
print()

print('API - Getting the Compliance Standard Requirements ...', end='')
pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_list_get(pc_settings, compliance_standard_original['id'])
compliance_requirement_list_original = response_package['data']
export_file_data['compliance_requirement_list_original'] = compliance_requirement_list_original
print(' done.')
print()

print('API - Getting the Compliance Standard Sections ...', end='')
for compliance_requirement_original in compliance_requirement_list_original:
    pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_section_list_get(pc_settings, compliance_requirement_original['id'])
    compliance_section_list_original = response_package['data']
    export_file_data['compliance_section_list_original'][compliance_requirement_original['id']] = compliance_section_list_original
print(' done.')
print()

print('API - Getting the Compliance Standard Policies ...', end='')
pc_settings, response_package = pc_lib_api.api_compliance_standard_policy_v2_list_get(pc_settings, compliance_standard_original['name'])
policy_list_original = response_package['data']
export_file_data['policy_list_original'] = policy_list_original
print(' done.')
print()

print('API - Getting the Policies (please wait) ...', end='')
for policy_original in policy_list_original:
    pc_settings, response_package = pc_lib_api.api_policy_get(pc_settings, policy_original['policyId'])
    policy = response_package['data']
    export_file_data['policy_object_original'][policy_original['policyId']] = policy
    # Anomaly Policies (policy_original['rule']['type'] == 'Anomaly') do not have 'parameters'.
    if not 'parameters' in policy_original['rule']:
        continue
    if policy_original['rule']['parameters']['savedSearch'] == 'true':
        if policy_original['rule']['criteria'] not in export_file_data['search_object_original']:
            pc_settings, response_package = pc_lib_api.api_search_get(pc_settings, policy_original['rule']['criteria'])
            search_object_original = response_package['data']
            export_file_data['search_object_original'][policy_original['rule']['criteria']] = search_object_original
print(' done.')
print()

pc_lib_general.pc_file_write_json(args.export_file_name, export_file_data)
print('Compliance Standard exported to: %s' % args.export_file_name)
print()
