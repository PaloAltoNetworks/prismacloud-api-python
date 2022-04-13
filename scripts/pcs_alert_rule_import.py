""" Import Alert Rules """

import json

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

CUSTOM_POLICY_ID_MAP_FILE = 'PolicyIdMap.json'

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--alert_rule',
    type=str,
    help='(Optional) - Import a single Alert Rule with the given name'
)
parser.add_argument(
    '--update_existing',
    action='store_true',
    help='(Optional) - Update the Alert Rule, if it exists.'
    )
parser.add_argument(
    '--skip_existing',
    action='store_true',
    help='(Optional) - Skip the Alert Rule, if it exists rather than erroring out.'
    )
parser.add_argument(
    '--skip_missing_policies',
    action='store_true',
    help='(Optional) - Skip the policies that do not exist in the new tenant rather than erroring out.'
    )
parser.add_argument(
    '--skip_missing_account_group',
    action='store_true',
    help='(Optional) - Skip the account groups that do not exist in the new tenant rather than erroring out.'
    )
parser.add_argument(
    '--skip_notifications',
    action='store_true',
    help='(Optional) - Skip third party notifications when creating the imported rule.'
)
parser.add_argument(
    '--use_default_account_group',
    action='store_true',
    help='(Optional) - Use Default Account Group instead of those listed in export file. Useful when copying an alert rule to a new tenant with different accounts/account groups.'
    )
parser.add_argument(
    'import_file_name',
    type=str,
    help='Import file name for Alert Rules.'
    )
args = parser.parse_args()

# --Initialize-- #

pc_utility.prompt_for_verification_to_continue(args)
settings = pc_utility.get_settings(args)
pc_api.configure(settings)

try:
    custom_policy_id_map = json.load(open(CUSTOM_POLICY_ID_MAP_FILE, 'r'))
except (ValueError, FileNotFoundError):
    custom_policy_id_map = {}


# --Main-- #

# Alert Rule Import

import_file_data = pc_utility.read_json_file(args.import_file_name)

# Validation
if 'alert_rule_list_original' not in import_file_data:
    pc_utility.error_and_exit(404, 'alert_rule_list_original section not found. Please verify the import file and name.')

alert_rule_list_original = import_file_data['alert_rule_list_original']
if alert_rule_list_original is None:
    pc_utility.error_and_exit(400, 'Alert Rules not found in the import file. Please verify the import file and name.')
if args.alert_rule:
    alert_rule_export = False
    for alert_rule_original in alert_rule_list_original:
        if alert_rule_original['name'] == args.alert_rule:
            alert_rule_export = True
    if not alert_rule_export:
        pc_utility.error_and_exit(400, 'Alert Rule not found in the import file. Please verify the import file and it\'s contents.')

# Alert Rules

print('API - Getting list of Alert Rules ...', end='')
alert_rule_list = pc_api.alert_rule_list_read()
print(' done.')
print()

print('API - Getting list of Policies ...', end='')
policy_new_list = pc_api.policy_v2_list_read()
print(' done.')
print()

print('API - Getting list of Account Groups ...', end='')
account_groups_new_list = pc_api.cloud_account_group_list_read()
print(' done.')
print()

if args.update_existing:
    print('API - Adding/Updating Alert Rules ...')
else:
    print('API - Adding Alert Rules ...')

added = 0
updated = 0
skipped = 0

for alert_rule_original in alert_rule_list_original:
    print(f'{alert_rule_original["name"]} ... ', end='')
    alert_rule_method = 'create'
    alert_rule_update_id = None
    # See if an Alert Rule with the same name already exists
    for alert_rule in alert_rule_list:
        if alert_rule['name'] == alert_rule_original['name']:
            if args.update_existing:
                alert_rule_method = 'update'
                alert_rule_update_id = alert_rule['policyScanConfigId']
            elif args.skip_existing:
                alert_rule_method = 'skip'
            else:
                pc_utility.error_and_exit(400, 'Alert Rule already exists. Please verify the new Alert Rule name, or delete the existing AlertRule.')
    # Add/update Alert Rule
    if alert_rule_method == 'skip':
        skipped += 1
        print(' skipped.')
        continue

    # Verify Policies
    new_policies_list = []
    for policy_original_id in alert_rule_original['policies']:
        # First see if there is mapping in PolicyIdMap
        old_policy_id = policy_original_id
        if policy_original_id in custom_policy_id_map:
            new_policy_id = custom_policy_id_map[old_policy_id]
        else:
            new_policy_id = old_policy_id
        policy_found = False
        for policy_new in policy_new_list:
            if policy_new['policyId'] == new_policy_id:
                policy_found = True
                break
        if not policy_found:
            if not args.skip_missing_policies:
                pc_utility.error_and_exit(400, f'Policy not found in new tenant ({new_policy_id}). You might need to export custom Policies from the old tenant and import them to the new tenant first.')
            continue
        new_policies_list.append(new_policy_id)
    alert_rule_original['policies'] = new_policies_list

    # Verify Account Groups
    default_account_group_new = None
    new_account_group_list = []
    if args.use_default_account_group:
        for account_group_new in account_groups_new_list:
            if account_group_new['name'] == "Default Account Group":
                default_account_group_new_id = account_group_new['id']
        if not default_account_group_new:
            pc_utility.error_and_exit(400, 'Could not find Default Account Group')
        new_account_group_list = [default_account_group_new_id]
    else:
        for account_group_original_id in alert_rule_original['target']['accountGroups']:
            account_group_found = False
            for account_group_new in account_groups_new_list:
                if account_group_original_id == account_group_new['id']:
                    account_group_found = True
                    break
            if not account_group_found:
                if not args.skip_missing_account_groups:
                    pc_utility.error_and_exit(400, f'Account Group not found in new tenant ({account_group_original_id}). You might need to export Account Groups from the old tenant and import them to the new tenant first.')
                continue
            new_account_group_list.append(account_group_original_id)
    alert_rule_original['target']['accountGroups'] = new_account_group_list

    # Skip Notifications
    if args.skip_notifications:
        alert_rule_original['notificationChannels'] = []
    if alert_rule_method == 'create':
        del alert_rule_original['policyScanConfigId']
        pc_api.alert_rule_create(alert_rule_original)
        added += 1
        print(' added.')
    elif alert_rule_method == 'update':
        pc_api.alert_rule_update(alert_rule_update_id, alert_rule_original)
        updated += 1
        print(' updated.')
print()
print('Import Complete.')
print(f'Summary: {added} added, {updated} updated, {skipped} skipped.')
