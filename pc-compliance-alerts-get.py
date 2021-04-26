from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import pc_lib_api
import pc_lib_general
import json

# --Configuration-- #

parser = pc_lib_general.pc_arg_parser_defaults()
parser.add_argument(
    'compliance_standard_name',
    type=str,
    help='Name of the Compliance Standard.')
parser.add_argument(
    'cloud_account_name',
    type=str,
    help='Name of the Cloud Account.')
args = parser.parse_args()

# --Main-- #

pc_lib_general.prompt_for_verification_to_continue(args.yes)

print('API - Getting login ...', end='')
pc_settings = pc_lib_general.pc_settings_get(args.username, args.password, args.uiurl, args.config_file)
pc_settings = pc_lib_api.pc_login(pc_settings)
print(' done.')
print()

# COMPLIANCE ALERTS GET

compliance_standard_name = args.compliance_standard_name
cloud_account_name = args.cloud_account_name

alert_detail     = True
alert_status     = 'open'
time_range_type  = 'to_now'
time_range_value = 'epoch'

print('API - Getting the Compliance Standard Policy list ...', end='')
pc_settings, response_package = pc_lib_api.api_compliance_standard_policy_list_get(pc_settings, compliance_standard_name)
compliance_standard_policy_list = response_package['data']
print(' done.')
print()

# Loop through the Policy list to collect the related Alerts for the Cloud Account.
alert_list = []
for compliance_policy in compliance_standard_policy_list:
    alert_filter = {'detailed': alert_detail,
                    'timeRange': {'type': time_range_type, 'value': time_range_value},
                    'filters': [{'operator': '=', 'name': 'alert.status', 'value': alert_status},
                                {'operator': '=', 'name': 'cloud.account', 'value': cloud_account_name},
                                {'name': 'policy.id', 'operator': '=', 'value': compliance_policy['policyId']}]}
    print('API - Getting the Alerts for Policy: %s ...' % compliance_policy['name'], end='')
    pc_settings, response_package = pc_lib_api.api_alert_list_get(pc_settings, data=alert_filter)
    alert_list.extend(response_package['data'])
    print(' done.')
    print()

print('Alerts:')
print(json.dumps(alert_list))
