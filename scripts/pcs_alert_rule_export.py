""" Export Alert Rules """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--alert_rule',
    type=str,
    help='(Optional) - Export a single Alert Rule with the given name'
)
parser.add_argument(
    'export_file_name',
    type=str,
    help='Export file name for the Alert Rules.'
)
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

# Alert Rule Export

export_file_data = {}
export_file_data['alert_rule_list_original'] = []

print('API - Getting list of Alert Rules ...', end='')
alert_rule_list = pc_api.alert_rule_list_read()
if args.alert_rule:
    for alert_rule in alert_rule_list:
        if alert_rule.get('name') == args.alert_rule:
            export_file_data['alert_rule_list_original'] = [alert_rule]
else:
    export_file_data['alert_rule_list_original'] = alert_rule_list
print(' done.')
print()

print('Writing export file ...', end='')
pc_utility.write_json_file(args.export_file_name, export_file_data)
print(' done.')
print()
