""" Get a list of Alerts """

import json

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--detailed',
    action='store_true',
    help='(Optional) - Get Alert details.')
parser.add_argument(
    '-fas',
    '--alertstatus',
    type=str,
    choices=['open', 'resolved', 'snoozed', 'dismissed'],
    help='(Optional) - Filter - Alert Status.')
parser.add_argument(
    '-fpt',
    '--policytype',
    type=str,
    help='(Optional) - Filter - Policy Type.')
parser.add_argument(
    '-fpn',
    '--policyname',
    type=str,
    help='(Optional) - Filter - Policy Name.')
parser.add_argument(
    '-tr',
    '--timerange',
    type=int,
    default=30,
    help='(Optional) - Time Range in days (default 30).')
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

# ALERT GET

# Sort out and build the filters.

alerts_filter = {}
if args.detailed:
    alerts_filter['detailed'] = True
else:
    alerts_filter['detailed'] = False
alerts_filter['filters'] = []
alerts_filter['limit'] = 1000
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
if args.policyname is not None:
    temp_filter = {}
    temp_filter['name']     = 'policy.name'
    temp_filter['operator'] = '='
    temp_filter['value']    = args.policyname
    alerts_filter['filters'].append(temp_filter)

print('API - Getting the Alerts list ...', end='')
alerts_list = pc_api.alert_v2_list_read(body_params=alerts_filter)
print(' done.')
print()

print('Alerts:')
print(json.dumps(alerts_list))
