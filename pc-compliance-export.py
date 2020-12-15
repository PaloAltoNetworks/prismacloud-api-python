from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import pc_lib_api
import pc_lib_general


# --Configuration-- #
# Import file version expected
DEFAULT_COMPLIANCE_EXPORT_FILE_VERSION = 3


# --Helper Functions (Local)-- #
def search_list_object_lower(list_to_search, field_to_search, search_value):
    object_to_return = None
    search_value = search_value.lower()
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search].lower() == search_value:
                object_to_return = source_item
                break
    return object_to_return


# --Execution Block-- #
# --Parse command line arguments-- #
parser = pc_lib_general.pc_arg_parser_defaults()

parser.add_argument(
    'source_compliance_standard_name',
    type=str,
    help='Name of the compliance standard to copy from.  Please enter it exactly as listed in the Prisma Cloud UI')

parser.add_argument(
    'export_file_name',
    type=str,
    help='Name of the new compliance standard to create.')

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

## Compliance Copy ##
# Set up the data structure
export_file_data = {}
export_file_data['export_file_version'] = DEFAULT_COMPLIANCE_EXPORT_FILE_VERSION
export_file_data['compliance_section_list_original'] = {}
export_file_data['policy_object_original'] = {}
export_file_data['search_object_original'] = {}
export_file_data['policy_list_original'] = []

# Check the compliance standard and get the JSON information
print('API - Getting the Compliance Standards list...')
pc_settings, response_package = pc_lib_api.api_compliance_standard_list_get(pc_settings)
compliance_standard_list_temp = response_package['data']
compliance_standard_original = search_list_object_lower(compliance_standard_list_temp, 'name', args.source_compliance_standard_name)
if compliance_standard_original is None:
    pc_lib_general.pc_exit_error(400, 'Compliance Standard not found.  Please check the Compliance Standard name and try again.')
export_file_data['compliance_standard_original'] = compliance_standard_original
print(' Done.')
print()

# Get the list of requirements that need to be exported
print('API - Getting Compliance Standard Requirements...')
pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_list_get(pc_settings, compliance_standard_original['id'])
compliance_requirement_list_original = response_package['data']
export_file_data['compliance_requirement_list_original'] = compliance_requirement_list_original
print(' Done.')
print()

# Get list of sections and export for each requirement section
print('API - Get list of sections...')
for compliance_requirement_original_temp in compliance_requirement_list_original:
    # Get sections for requirement
    pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_section_list_get(pc_settings, compliance_requirement_original_temp['id'])
    compliance_section_list_original_temp = response_package['data']
    export_file_data['compliance_section_list_original'][compliance_requirement_original_temp['id']] = compliance_section_list_original_temp
print(' Done.')
print()

# Get the associated policies
print('API - Getting the compliance standard policy list...')
pc_settings, response_package = pc_lib_api.api_compliance_standard_policy_v2_list_get(pc_settings, compliance_standard_original['name'])
policy_list_original = response_package['data']
export_file_data['policy_list_original'] = policy_list_original
print(' Done.')
print()

# Get the individual policy objects in case something needs to be added for import
print('API - Individual policy retrieval (might take a while)...')
for policy_original_temp in policy_list_original:
    # Get the individual policy JSON object
    pc_settings, response_package = pc_lib_api.api_policy_get(pc_settings, policy_original_temp['policyId'])
    policy_specific_temp = response_package['data']
    export_file_data['policy_object_original'][policy_original_temp['policyId']] = policy_specific_temp
    # Get the related saved search object (if needed)
    if policy_original_temp['rule']['parameters']['savedSearch'] == "true":
        if policy_original_temp['rule']['criteria'] not in export_file_data['search_object_original']:
            pc_settings, response_package = pc_lib_api.api_search_get(pc_settings, policy_original_temp['rule']['criteria'])
            search_specific_temp = response_package['data']
            export_file_data['search_object_original'][policy_original_temp['rule']['criteria']] = search_specific_temp
print(' Done.')
print()

# Save compliance standard to file
print('FILE - Saving Compliance Standard to a file...')
pc_lib_general.pc_file_write_json(args.export_file_name, export_file_data)
print(' File saved to ' + args.export_file_name)
