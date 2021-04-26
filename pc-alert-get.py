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
    '--detailed',
    action='store_true',
    help='(Optional) - Get Alert details.')
parser.add_argument(
    '-fas',
    '--alertstatus',
    type=str,
    help='(Optional) - Filter - Alert Status.')
parser.add_argument(
    '-fpt',
    '--policytype',
    type=str,
    help='(Optional) - Filter - Policy Type.')
parser.add_argument(
    '-tr',
    '--timerange',
    type=int,
    default=30,
    help='(Optional) - Time Range in days (default 30).')
parser.add_argument(
    '-l',
    '--limit',
    type=int,
    default=500,
    help='(Optional) - Limit the number of Alerts to get (default 500).')
args = parser.parse_args()

# --Main-- #

pc_lib_general.prompt_for_verification_to_continue(args.yes)

print('API - Getting login ...', end='')
pc_settings = pc_lib_general.pc_settings_get(args.username, args.password, args.uiurl, args.config_file)
pc_settings = pc_lib_api.pc_login(pc_settings)
print(' done.')
print()

# ALERT GET

# Sort out and build the filters.

alerts_filter = {}
if args.detailed:
    alerts_filter['detailed'] = True
else:
    alerts_filter['detailed'] = False
alerts_filter['filters'] = []
alerts_filter['limit'] = args.limit
alerts_filter['offset'] = 0
alerts_filter['sortBy'] = ['id:asc']
alerts_filter['timeRange'] = {}
alerts_filter['timeRange']['type']            = 'relative'
alerts_filter['timeRange']['value']           = {}
alerts_filter['timeRange']['value']['unit']   = 'day'
alerts_filter['timeRange']['value']['amount'] = args.timerange
if args.alertstatus is not None:
    temp_filter = {}
    temp_filter['name']     = 'alert.status'
    temp_filter['operator'] = '='
    temp_filter['value']    = args.alertstatus
    alerts_filter['filters'].append(temp_filter)
if args.policytype is not None:
    temp_filter = {}
    temp_filter['name']     = 'policy.type'
    temp_filter['operator'] = '='
    temp_filter['value']    = args.policytype
    alerts_filter['filters'].append(temp_filter)

print('API - Getting the Alerts list ...', end='')
pc_settings, response_package = pc_lib_api.api_alert_v2_list_get(pc_settings, data=alerts_filter)
alerts_list = response_package['data']
print(' done.')
print()

print('Alerts:')
print(json.dumps(alerts_list))
