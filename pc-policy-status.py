from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import pc_lib_general
import pc_lib_api


# --Execution Block-- #
# --Parse command line arguments-- #
parser = pc_lib_general.pc_arg_parser_defaults()
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument(
    '-t',
    '--policy_type',
    type=str,
    choices=['config', 'network', 'audit_event', 'anomaly', 'all'],
    help='Policies to enable or disable, by policy type.')

group.add_argument(
    '-s',
    '--compliance_standard',
    type=str,
    help='Policies to enable or disable, by compliance standard.')

parser.add_argument(
    'status',
    type=str,
    choices=['enable', 'disable'],
    help='Policy status to set (enable or disable).')

args = parser.parse_args()
# --End parse command line arguments-- #

# --Main-- #
# Get login details worked out
pc_settings = pc_lib_general.pc_login_get(args.username, args.password, args.uiurl)

# Verification (override with -y)
if not args.yes:
    print()
    print('Ready to execute commands aginst your Prisma Cloud tenant.')
    verification_response = str(input('Would you like to continue (y or yes to continue)?'))
    continue_response = {'yes', 'y'}
    print()
    if verification_response not in continue_response:
        pc_lib_general.pc_exit_error(400, 'Verification failed due to user response. Exiting ...')

# Sort out API Login
print('API - Getting authentication token ... ', end='')
pc_settings = pc_lib_api.pc_jwt_get(pc_settings)
print('Done.')

# Transform the status argument for use with Python and the API.
specified_policy_status = True if args.status.lower() == 'enable' else False
specified_policy_status_str = str(specified_policy_status).lower()

policy_list_to_update = []

# Filter policies by one policy type, or no filter: all policy types.
if args.policy_type is not None:
    policy_type = args.policy_type.lower()
    print('API - Getting list of policies ... ', end='')
    pc_settings, response_package = pc_lib_api.api_policy_v2_list_get(pc_settings)
    policy_list = response_package['data']
    print('Done.')
    print('Filtering policy list for specified policy type of "' + policy_type + '" ... ', end='')
    for this_policy in policy_list:
        # print('API - Debug - Policy: ' + this_policy['name'] + ' => ' + str(this_policy['enabled']))
        if this_policy['enabled'] is not specified_policy_status:
            if policy_type == "all":
                policy_list_to_update.append(this_policy)
            elif this_policy['policyType'] == policy_type:
                policy_list_to_update.append(this_policy)
    print('Done.')

# Filter policies by one compliance standard.
if args.compliance_standard is not None:
    compliance_standard = args.compliance_standard
    print('API - Getting list of policies ... ', end='')
    pc_settings, response_package = pc_lib_api.api_compliance_standard_policy_v2_list_get(pc_settings, compliance_standard)
    policy_list = response_package['data']
    print('Done.')
    print('Filtering policy list for specified compliance standard of "' + compliance_standard + '" ... ', end='')
    for this_policy in policy_list:
        # print('API - Debug - Policy: ' + this_policy['name'] + ' => ' + str(this_policy['enabled']))
        if this_policy['enabled'] is not specified_policy_status:
            policy_list_to_update.append(this_policy)
    print('Done.')

print('API - Updating policy statuses ... ')
for this_policy in policy_list_to_update:
    print('API - Updating policy: ' + this_policy['name'])
    pc_settings, response_package = pc_lib_api.api_policy_status_update(pc_settings, this_policy['policyId'], specified_policy_status_str)
print('Done.')