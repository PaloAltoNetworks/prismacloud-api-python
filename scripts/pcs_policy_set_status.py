""" Set the Status (enable or disable) of a Policy """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    '--all_policies',
    action='store_true',
    help='Enable or disable all Policies.')
group.add_argument(
    '--cloud_type',
    type=str,
    choices=['aws', 'azure', 'gcp', 'oci', 'alibaba_cloud'],
    help='Enable or disable Policies by Cloud Type.')
group.add_argument(
    '--policy_severity',
    type=str,
    choices=['low', 'medium', 'high'],
    help='Enable or disable Policies by Policy Severity.')
group.add_argument(
    '--policy_type',
    type=str,
    choices=['config', 'network', 'audit_event', 'anomaly'],
    help='Enable or disable Policies by Policy Type.')
group.add_argument(
    '-s',
    '--compliance_standard',
    type=str,
    help='Enable or disable Policies by Compliance Standard.')
parser.add_argument(
    'status',
    type=str,
    choices=['enable', 'disable'],
    help='Policy status to set (enable or disable).')
args = parser.parse_args()

# --Initialize-- #

pc_utility.prompt_for_verification_to_continue(args)
settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

# Transform the status argument for use with Python and the API.
specified_policy_status = bool(args.status.lower() == 'enable')
specified_policy_status_string = str(specified_policy_status).lower()

policy_list_to_update = []

if args.compliance_standard is not None:
    compliance_standard = args.compliance_standard
    print('API - Getting list of Policies by Compliance Standard (%s) ...' % compliance_standard, end='')
    policy_list = pc_api.compliance_standard_policy_v2_list_read(compliance_standard)
    print(' done.')
    for policy in policy_list:
        # Do not update a policy if it is already in the desired state.
        if policy['enabled'] is not specified_policy_status:
            policy_list_to_update.append(policy)
else:
    print('API - Getting list of Policies ...', end='')
    policy_list = pc_api.policy_v2_list_read()
    print(' done.')
    print()
    if args.all_policies:
        for policy in policy_list:
            # Do not update a policy if it is already in the desired state.
            if policy['enabled'] is not specified_policy_status:
                policy_list_to_update.append(policy)
    elif args.cloud_type is not None:
        cloud_type = args.cloud_type.lower()
        for policy in policy_list:
            if policy['enabled'] is not specified_policy_status:
                if cloud_type == policy['cloudType']:
                    policy_list_to_update.append(policy)
    elif args.policy_severity is not None:
        policy_severity = args.policy_severity.lower()
        for policy in policy_list:
            if policy['enabled'] is not specified_policy_status:
                if policy_severity == policy['severity']:
                    policy_list_to_update.append(policy)
    elif args.policy_type is not None:
        policy_type = args.policy_type.lower()
        for policy in policy_list:
            if policy['enabled'] is not specified_policy_status:
                if policy_type == policy['policyType']:
                    policy_list_to_update.append(policy)

if policy_list_to_update:
    print('API - Updating Policies ...')
    for policy in policy_list_to_update:
        print('API - Updating Policy: %s' % policy['name'])
        pc_api.policy_status_update(policy['policyId'], specified_policy_status_string)
    print('Done.')
    print()
else:
    print('API - No Policies match the specified parameter, or all matching Policies are already enabled or disabled.')
    print()
