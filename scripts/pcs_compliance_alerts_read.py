""" Get a list of Alerts for a specific Compliance Standard and Cloud Account """

import json

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    'compliance_standard_name',
    type=str,
    help='Name of the Compliance Standard.')
parser.add_argument(
    'cloud_account_name',
    type=str,
    help='Name of the Cloud Account.')
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

# COMPLIANCE ALERTS GET

compliance_standard_name = args.compliance_standard_name
cloud_account_name = args.cloud_account_name

alert_detail     = True
alert_status     = 'open'
time_range_type  = 'to_now'
time_range_value = 'epoch'

print('API - Getting the Compliance Standard Policy list ...', end='')
compliance_standard_policy_list = pc_api.compliance_standard_policy_list_read(compliance_standard_name)
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
    filtered_alert_list = pc_api.alert_list_read(body_params=alert_filter)
    alert_list.extend(filtered_alert_list)
    print(' done.')
    print()

print('Alerts:')
print(json.dumps(alert_list))
