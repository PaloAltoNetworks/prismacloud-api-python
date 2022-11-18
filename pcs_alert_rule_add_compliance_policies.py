""" Add Policies to an alert rule based on compliance standard """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    'alert_rule_name',
    type=str,
    help='Name of the Alert Rule to update'
)
parser.add_argument(
    'compliance_standard_name',
    type=str,
    help='Name of the Compliance Standard to add Policies from'
)
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

# Get Compliance policies

print('API - Getting list of Policies by Compliance Standard ...', end='')
policy_list = pc_api.compliance_standard_policy_v2_list_read(args.compliance_standard_name)
compliance_policy_ids = []
for policy in policy_list:
    compliance_policy_ids.append(policy['policyId'])
print(' done.')
print()

# Get Alert Rule

print('API - Getting list of Alert Rules ...', end='')
alert_rule_list = pc_api.alert_rule_list_read()
for alert_rule in alert_rule_list:
    if alert_rule.get('name') == args.alert_rule_name:
        alert_rule_original = alert_rule
print(' done.')
print()

# Update Alert Rule
print('API - Updating Alert Rule with new Policy list ...', end='')
alert_rule_original['policies'] = alert_rule_original.get('policies', []) + compliance_policy_ids
pc_api.alert_rule_update(alert_rule_original['policyScanConfigId'], alert_rule_original)
print(' done.')
print()
