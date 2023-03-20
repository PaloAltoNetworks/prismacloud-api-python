""" Set the Status (enable or disable) of a Policy """

import sys

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--all_policies',
    action='store_true',
    help='Enable or disable all Policies')
parser.add_argument(
    '--cloud_type',
    type=str,
    choices=['aws', 'azure', 'gcp', 'oci', 'alibaba_cloud'],
    help='Enable or disable Policies by Cloud Type')
parser.add_argument(
    '--compliance_standard',
    type=str,
    help='Enable or disable Policies by Compliance Standard (ignore other selectors)')
parser.add_argument(
    '--policy_severity',
    type=str,
    choices=['informational', 'low', 'medium', 'high', 'critical'],
    help='Enable or disable Policies by Severity')
parser.add_argument(
    '--policy_type',
    type=str,
    choices=['anomaly', 'attack_path', 'audit_event', 'config', 'data', 'iam', 'network', 'workload_incident', 'workload_vulnerability'],
    help='Enable or disable Policies by Type')
parser.add_argument(
    '--policy_subtype',
    type=str,
    choices=['build', 'run'],
    help='Enable or disable Policies by Subtype')
parser.add_argument(
    '--policy_descriptor',
    type=str,
    choices=['PC-ALL-ALL', 'PC-AWS', 'PC-GCP', 'PC-AZR', 'PC-OCI', 'PC-ALB', 'blank'],
    help='Enable or disable Policies by Descriptor')
parser.add_argument(
    '--policy_label',
    type=str,
    choices=['Prisma_Cloud'],
    help='Enable or disable Policies by Labels')
parser.add_argument(
    '--policy_mode',
    type=str,
    choices=['Default', 'Custom'],
    help='Enable or disable Policies by Mode - Default or Custom')
parser.add_argument(
    '--merge',
    action='store_true',
    help='Enable or disable Policies based upon a merge of all selectors (excluding Compliance Standard)')
parser.add_argument(
    'status',
    type=str,
    choices=['enable', 'disable'],
    help="Policy Status to set ('enable' or 'disable')")
args = parser.parse_args()

# --Initialize-- #

pc_utility.prompt_for_verification_to_continue(args)

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# Transform selectors.

policy_selector_list = []
if args.cloud_type is not None:
    policy_selector_list.append({'selector_name': 'cloud_type', 'selector_value': args.cloud_type.lower()})
if args.policy_severity is not None:
    policy_selector_list.append({'selector_name': 'policy_severity', 'selector_value': args.policy_severity.lower()})
if args.policy_type is not None:
    policy_selector_list.append({'selector_name': 'policy_type', 'selector_value': args.policy_type.lower()})
if args.policy_subtype is not None:
    policy_selector_list.append({'selector_name': 'policy_subtype', 'selector_value': args.policy_subtype.lower()})
if args.policy_mode is not None:
    policy_selector_list.append({'selector_name': 'policy_mode', 'selector_value': args.policy_mode.lower()})
if args.policy_label is not None:
    policy_selector_list.append({'selector_name': 'policy_label', 'selector_value': args.policy_label})
if args.policy_descriptor is not None:
    policy_selector_list.append({'selector_name': 'policy_descriptor', 'selector_value': args.policy_descriptor})

if len(policy_selector_list) > 1 and args.merge is False:
    print("Error: Please specify '--merge' when specifying multple selectors.")
    sys.exit(0)

# Transform the status argument for use with Python and the API.

policy_status = bool(args.status.lower() == 'enable')
policy_status_string = str(policy_status).lower()

# --Helpers-- #

def policy_matches(this_policy, this_selector_name, this_selector_value):
    if not this_selector_value:
        return False
    if this_selector_name == 'cloud_type' and this_selector_value == policy['cloudType']:
        return True
    if this_selector_name == 'policy_severity' and this_selector_value == policy['severity']:
        return True
    if this_selector_name == 'policy_type' and this_selector_value == policy['policyType']:
        return True
    if this_selector_name == 'policy_subtype' and this_selector_value in policy['policySubTypes']:
        return True
    if this_selector_name == 'policy_mode' and this_selector_value == policy['policyMode']:
        return True
    if this_selector_name == 'policy_label' and this_selector_value in policy['labels']:
        return True
    if this_selector_name == 'policy_descriptor':
        if 'policyUpi' in this_policy:
            return this_policy['policyUpi'].startswith(this_selector_value)
        return this_selector_value == 'blank'
    return False

##

def update_policies(this_policy_list, this_policy_status, this_policy_status_string):
    if this_policy_list:
        print('API - Evaluating %s Policies ...' % len(this_policy_list))
        counter=0
        for this_policy in this_policy_list:
            # Do not update a policy if it is already in the desired status.
            if this_policy['enabled'] is this_policy_status:
                print('Skipping Policy with matching status (%s / %s): %s' % (this_policy_status, this_policy['enabled'], this_policy['name']))
                continue
            counter+=1
            print('API - Updating Policy: %s' % this_policy['name'])
            pc_api.policy_status_update(this_policy['policyId'], this_policy_status_string)
            if counter % 10 == 0:
                print('Progress: %.0f%% ' % (int(counter) / int(len(this_policy_list))*100))
        print('Done.')
        print()
    else:
        print('API - No Policies match the specified parameters.')
        print()

# --Main-- #

if args.compliance_standard is None:
    print('API - Getting list of Policies ...', end='')
    policy_list = pc_api.policy_v2_list_read()
else:
    print('API - Getting list of Policies by Compliance Standard (%s) ...' % args.compliance_standard, end='')
    policy_list = pc_api.compliance_standard_policy_v2_list_read(args.compliance_standard)
print(' done.')
print()

if args.all_policies:
    update_policies(policy_list, policy_status, policy_status_string)
    sys.exit(0)

selected_policies = []
for policy in policy_list:
    selector_matches_list = []
    for policy_selector in policy_selector_list:
        if policy_matches(policy, policy_selector['selector_name'], policy_selector['selector_value']):
            selector_matches_list.append(policy_selector['selector_name'])
    if len(selector_matches_list) == len(policy_selector_list):
        selected_policies.append(policy)
update_policies(selected_policies, policy_status, policy_status_string)
