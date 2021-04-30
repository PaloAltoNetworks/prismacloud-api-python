from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
from pc_lib_api import pc_api
import pc_lib_general
import concurrent.futures

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

pc_lib_general.prompt_for_verification_to_continue(args)
pc_settings = pc_lib_general.pc_settings_get(args)
pc_api.configure(pc_settings)

# --Threading-- #

thread_pool_executor = concurrent.futures.ThreadPoolExecutor(16)

def threaded_policy_get(policy_current):
    print('Getting Policy: %s' % policy_current['name'])
    return pc_api.policy_get(policy_current['policyId'])

def threaded_saved_search_get(policy_current):
    print('Getting Saved Search: %s' % policy_current['name'])
    return pc_api.saved_search_get(policy_current['rule']['criteria'])

# --Main-- #

# Compliance Export

export_file_data = {}
export_file_data['export_file_version'] = DEFAULT_COMPLIANCE_EXPORT_FILE_VERSION
export_file_data['compliance_section_list_original'] = {}
export_file_data['policy_list_original'] = []
export_file_data['policy_object_original'] = {}
export_file_data['search_object_original'] = {}

print('API - Getting the current list of Compliance Standards ...', end='')
compliance_standard_list_current = pc_api.compliance_standard_list_get()
compliance_standard_original = pc_lib_general.search_list_object_lower(compliance_standard_list_current, 'name', args.compliance_standard_name)
if compliance_standard_original is None:
    pc_lib_general.pc_exit_error(400, 'Compliance Standard to export not found. Please verify the Compliance Standard name.')
export_file_data['compliance_standard_original'] = compliance_standard_original
print(' done.')
print()

print('API - Getting the Compliance Standard Requirements ...', end='')
compliance_requirement_list_original = pc_api.compliance_standard_requirement_list_get(compliance_standard_original['id'])
export_file_data['compliance_requirement_list_original'] = compliance_requirement_list_original
print(' done.')
print()

print('API - Getting the Compliance Standard Sections ...', end='')
for compliance_requirement_original in compliance_requirement_list_original:
    compliance_section_list_original = pc_api.compliance_standard_requirement_section_list_get(compliance_requirement_original['id'])
    export_file_data['compliance_section_list_original'][compliance_requirement_original['id']] = compliance_section_list_original
print(' done.')
print()

print('API - Getting the Compliance Standard Policy List (please wait) ...', end='')
policy_list_current = pc_api.compliance_standard_policy_v2_list_get(compliance_standard_original['name'])
export_file_data['policy_list_original'] = policy_list_current
print(' done.')
print()

# Same as in pc-policy-custom-export.py

print('API - Getting the Policies associated with the Compliance Standard ...')
futures = []
for policy_current in policy_list_current:
    print('Scheduling Policy Request: %s' % policy_current['name'])
    futures.append(thread_pool_executor.submit(threaded_policy_get, policy_current))
concurrent.futures.wait(futures)
for future in concurrent.futures.as_completed(futures):
    policy_current = future.result()
    export_file_data['policy_object_original'][policy_current['policyId']] = policy_current
print('Done.')
print()

print('API - Getting the Policies Saved Searches ...')
futures = []
for policy_current in policy_list_current:
    if not 'parameters' in policy_current['rule']:
        continue
    if not 'savedSearch' in policy_current['rule']['parameters']:
        continue
    if policy_current['rule']['parameters']['savedSearch'] == 'true':
        print('Scheduling Saved Search Request: %s' % policy_current['name'])
        futures.append(thread_pool_executor.submit(threaded_saved_search_get, policy_current))
concurrent.futures.wait(futures)
for future in concurrent.futures.as_completed(futures):
    saved_search = future.result()
    export_file_data['search_object_original'][saved_search['id']] = saved_search
print('Done.')
print()

pc_lib_general.pc_file_write_json(args.export_file_name, export_file_data)

print('Exported to: %s' % args.export_file_name)
