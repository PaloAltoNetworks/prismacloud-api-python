""" Get a list of Alerts """

import json

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    'query',
    type=str,
    help='RQL')
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

# Config:  "config from cloud.resource where api.name = 'aws-ec2-describe-instances'"
# Network: "network from vpc.flow_record where bytes > 0 AND threat.source = 'AutoFocus' AND threat.tag.group = 'Cryptominer'"
# Event:   "event from cloud.audit_logs where operation IN ( 'AddUserToGroup', 'AttachGroupPolicy', 'AttachUserPolicy' , 'AttachRolePolicy' , 'CreateAccessKey', 'CreateKeyPair', 'DeleteKeyPair', 'DeleteLogGroup' )"

if not args.query:
    pc_utility.error_and_exit(500, 'Please specify an RQL query.')

search_params = {}
search_params['limit'] = 100
search_params['timeRange'] = {}
search_params['timeRange']['type']            = 'relative'
search_params['timeRange']['value']           = {}
search_params['timeRange']['value']['unit']   = 'day'
search_params['timeRange']['value']['amount'] = args.timerange
search_params['withResourceJson'] = False
search_params['query'] = args.query

print('API - Getting the RQL results ...', end='')
if args.query.startswith('config from'):
    result_list = pc_api.search_config_read(search_params=search_params)
elif args.query.startswith('network from'):
    result_list = pc_api.search_network_read(search_params=search_params)
elif args.query.startswith('event from'):
    result_list = pc_api.search_event_read(search_params=search_params)
else:
    pc_utility.error_and_exit(500, 'Unknown RQL query type (limited to: config|network|event).')
print(' done.')
print()

print('Results:')
print(json.dumps(result_list))
print()

print('Result Count:')
print(len(result_list))
