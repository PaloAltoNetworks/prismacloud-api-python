""" Set the Status (enable or disable) of a Policy """

import sys

# pylint: disable=import-error
from prismacloudapi import pc_api, pc_utility

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
    help='Enable or disable Policies by Compliance Standard (ignoring other selectors)')
parser.add_argument(
    '--policy_severity',
    type=str,
    choices=['informational', 'low', 'medium', 'high', 'critical'],
    help='Enable or disable Policies by Severity')
parser.add_argument(
    '--policy_mode',
    type=str,
    choices=['Default', 'Custom'],
    help='Enable or disable Policies by Mode - Default or Custom')
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
    '--policy_label',
    type=str,
    choices=['Prisma_Cloud'],
    help='Enable or disable Policies by Labels')
parser.add_argument(
    '--policy_descriptor',
    type=str,
    choices=['PC-ALL-ALL', 'PC-AWS', 'PC-GCP', 'PC-AZR', 'PC-OCI', 'PC-ALB', 'blank'],
    help='Enable or disable Policies by Descriptor')
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

# --Helpers-- #

# Define policy selectors.

def policy_selectors(argz):
    result = []
    if argz.cloud_type is not None:
        result.append({'selector_name': 'cloud_type',        'selector_value': argz.cloud_type.lower()})
    if argz.policy_severity is not None:
        result.append({'selector_name': 'policy_severity',   'selector_value': argz.policy_severity.lower()})
    if argz.policy_mode is not None:
        result.append({'selector_name': 'policy_mode',       'selector_value': argz.policy_mode.lower()})
    if argz.policy_type is not None:
        result.append({'selector_name': 'policy_type',       'selector_value': argz.policy_type.lower()})
    if argz.policy_subtype is not None:
        result.append({'selector_name': 'policy_subtype',    'selector_value': argz.policy_subtype.lower()})
    if argz.policy_label is not None:
        result.append({'selector_name': 'policy_label',      'selector_value': argz.policy_label})
    if argz.policy_descriptor is not None:
        result.append({'selector_name': 'policy_descriptor', 'selector_value': argz.policy_descriptor})
    return result

# Evaluate policy selectors for a policy.

def policy_matches_selector(this_policy, this_selector_name, this_selector_value):
    if not this_selector_value:
        return False
    if this_selector_name == 'cloud_type'      and this_selector_value == policy['cloudType']:
        return True
    if this_selector_name == 'policy_severity' and this_selector_value == policy['severity']:
        return True
    if this_selector_name == 'policy_mode'     and this_selector_value == policy['policyMode']:
        return True
    if this_selector_name == 'policy_type'     and this_selector_value == policy['policyType']:
        return True
    if this_selector_name == 'policy_subtype'  and this_selector_value in policy['policySubTypes']:
        return True
    if this_selector_name == 'policy_label'    and this_selector_value in policy['labels']:
        return True
    if this_selector_name == 'policy_descriptor':
        if 'policyUpi' in this_policy:
            return this_policy['policyUpi'].startswith(this_selector_value)
        return this_selector_value == 'blank'
    return False

# Update a list of policies, enabling or disabling each.

def update_policies(this_policy_list, args_status):
    # Transform the status argument for use with Python and the API.
    policy_status = bool(args_status.lower() == 'enable')
    policy_status_string = str(policy_status).lower()
    if this_policy_list:
        print('API - Evaluating %s Policies ...' % len(this_policy_list))
        counter=0
        for this_policy in this_policy_list:
            counter+=1
            # Do not update a policy if it is already has the specified status.
            if this_policy['enabled'] is policy_status:
                print('Skipping Policy with specified status (%s / %s): %s' % (policy_status, this_policy['enabled'], this_policy['name']))
                continue
            print('API - Updating Policy: %s' % this_policy['name'])
            pc_api.policy_status_update(this_policy['policyId'], policy_status_string)
            if counter % 10 == 0:
                print('Progress: %.0f%% ' % (int(counter) / int(len(this_policy_list))*100))
        print('Done.')
        print()
    else:
        print('API - No Policies match the specified parameters.')
        print()

# --Main-- #

# Get all policies, or all policies mapped to a specific compliance standard.

if args.compliance_standard is None:
    print('API - Getting list of Policies ...', end='')
    policy_list = pc_api.policy_v2_list_read()
else:
    print('API - Getting list of Policies by Compliance Standard (%s) ...' % args.compliance_standard, end='')
    policy_list = pc_api.compliance_standard_policy_v2_list_read(args.compliance_standard)
print(' done.')
print()

# Optionally update all policies and exit early.

if args.all_policies:
    update_policies(policy_list, args.status)
    sys.exit(0)

# Otherwise, select and update selected policies.

policy_selector_list = policy_selectors(args)
selected_policies = []
for policy in policy_list:
    selector_matches_list = []
    for policy_selector in policy_selector_list:
        if policy_matches_selector(policy, policy_selector['selector_name'], policy_selector['selector_value']):
            selector_matches_list.append(policy_selector['selector_name'])
    if len(selector_matches_list) == len(policy_selector_list):
        selected_policies.append(policy)
update_policies(selected_policies, args.status)
