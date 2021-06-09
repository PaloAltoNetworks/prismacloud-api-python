""" Import Alert Rules """

from __future__ import print_function
from pc_lib import pc_api, pc_utility

# --Configuration-- #

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
    'import_file_name',
    type=str,
    help='Import file name for the AlertRules.'
    )
args = parser.parse_args()

# --Initialize-- #

pc_utility.prompt_for_verification_to_continue(args)
settings = pc_utility.get_settings(args)
pc_api.configure(settings)

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
    if alert_rule_export == False:
        pc_utility.error_and_exit(400, 'Alert Rule not found in the import file. Please verify the import file and it\'s contents.')

# Alert Rules

print('API - Getting list of Alert Rules ...', end='')
alert_rule_list = pc_api.alert_rule_list_read()
print(' done.')
print()

if args.update_existing:
    print('API - Adding/Updating Alert Rules ...', end='')
else:
    print('API - Adding Alert Rules ...', end='')
added = 0
updated = 0
skipped = 0
for alert_rule_original in alert_rule_list_original:
    alert_rule_method = 'create'
    alert_rule_update_id = None
    # See if an alert rule with the same name already exists
    for alert_rule in alert_rule_list:
        if alert_rule['name'] == alert_rule_original['name']:
            if args.update_existing:
                alert_rule_method = 'update'
                alert_rule_update_id = alert_rule['policyScanConfigId']
            elif args.skip_existing:
                alert_rule_method = 'skip'
            else:
                pc_utility.error_and_exit(400, 'Alert Rule already exists. Please verify the new Alert Rule name, or delete the existing AlertRule.')
    # Add/update alert rule
    if alert_rule_method == 'skip':
        skipped += 1
        continue
    elif alert_rule_method == 'create':
        pc_api.alert_rule_create(alert_rule_original)
        added += 1
    elif alert_rule_method == 'update':
        pc_api.alert_rule_update(alert_rule_update_id, alert_rule_original)
        updated += 1
print(' done.')
print()
print(f'Summary: {added} added, {updated} updated, {skipped} skipped.')