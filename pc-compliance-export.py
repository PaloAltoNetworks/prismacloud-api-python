from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
from pc_lib_api import pc_api
import pc_lib_api
import pc_lib_general

# --Configuration-- #

DEFAULT_COMPLIANCE_EXPORT_FILE_VERSION = 3

parser = pc_lib_general.pc_arg_parser_defaults()
parser.add_argument(
    'compliance_standard_name',
    type=str,
    help='Name of the Compliance Standard to export.')
parser.add_argument(
    'export_file_name',
    type=str,
    help='Export file name for the Compliance Standard.')
args = parser.parse_args()

# --Initialize-- #

pc_lib_general.prompt_for_verification_to_continue(args.yes)
pc_settings = pc_lib_general.pc_settings_get(args.username, args.password, args.uiurl, args.config_file)
pc_api.configure(pc_settings['apiBase'], pc_settings['username'], pc_settings['password'])

# --Main-- #

# Compliance Export

export_file_data = {}
export_file_data['export_file_version'] = DEFAULT_COMPLIANCE_EXPORT_FILE_VERSION
export_file_data['compliance_section_list_original'] = {}
export_file_data['policy_object_original'] = {}
export_file_data['policy_list_original'] = []
export_file_data['search_object_original'] = {}

print('API - Getting the current list of Compliance Standards ...', end='')
compliance_standard_list_current = pc_lib_api.api_compliance_standard_list_get()
compliance_standard_original = pc_lib_general.search_list_object_lower(compliance_standard_list_current, 'name', args.compliance_standard_name)
if compliance_standard_original is None:
    pc_lib_general.pc_exit_error(400, 'Compliance Standard to export not found. Please verify the Compliance Standard name.')
export_file_data['compliance_standard_original'] = compliance_standard_original
print(' done.')
print()

print('API - Getting the Compliance Standard Requirements ...', end='')
compliance_requirement_list_original = pc_lib_api.api_compliance_standard_requirement_list_get(compliance_standard_original['id'])
export_file_data['compliance_requirement_list_original'] = compliance_requirement_list_original
print(' done.')
print()

print('API - Getting the Compliance Standard Sections ...', end='')
for compliance_requirement_original in compliance_requirement_list_original:
    compliance_section_list_original = pc_lib_api.api_compliance_standard_requirement_section_list_get(compliance_requirement_original['id'])
    export_file_data['compliance_section_list_original'][compliance_requirement_original['id']] = compliance_section_list_original
print(' done.')
print()

print('API - Getting the Compliance Standard Policies (please wait) ...', end='')
policy_list_current = pc_lib_api.api_compliance_standard_policy_v2_list_get(compliance_standard_original['name'])
export_file_data['policy_list_original'] = policy_list_current
print(' done.')
print()

print('API - Getting the Policies (please wait) ...')
for policy_current in policy_list_current:
    print('Exporting: %s' % policy_current['name'])
    policy = pc_lib_api.api_policy_get(policy_current['policyId'])
    export_file_data['policy_object_original'][policy_current['policyId']] = policy
    # Anomaly Policies (policy_current['rule']['type'] == 'Anomaly') do not have 'parameters'.
    if not 'parameters' in policy_current['rule']:
        continue
    if policy_current['rule']['parameters']['savedSearch'] == 'true':
        if policy_current['rule']['criteria'] not in export_file_data['search_object_original']:
            search_object_original = pc_lib_api.api_search_get(policy_current['rule']['criteria'])
            export_file_data['search_object_original'][policy_current['rule']['criteria']] = search_object_original
print('Done.')
print()

pc_lib_general.pc_file_write_json(args.export_file_name, export_file_data)
print('Compliance Standard exported to: %s' % args.export_file_name)
