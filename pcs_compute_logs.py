""" Get a Count of Protected Containers """

from __future__ import print_function

import datetime
from dateutil import parser, tz

from pc_lib import pc_api, pc_utility

# --Configuration-- #

this_parser = pc_utility.get_arg_parser()
this_parser.add_argument(
    '--hours',
    type=int,
    default=1,
    help='(Optional) - Time period to collect, in hours, from now. (Default: 1)')
this_parser.add_argument(
    '--log_limit',
    type=int,
    default=32768,
    help='(Optional) - Number of console logs to collect, requires --console_logs. (Default: 32768)')
this_parser.add_argument(
    '--no_core_audits',
    action='store_false',
    help='(Optional) - Do not collect core audit data. (Default: disabled)')
this_parser.add_argument(
    '--host_forensic_activities',
    action='store_true',
    help='(Optional) - Collect Host Forensic Activity audit data. Warning: potentially high volume/slow. (Default: disabled)')
this_parser.add_argument(
    '--console_logs',
    action='store_true',
    help='(Optional) - Collect Console logs. (Default: disabled)')
args = this_parser.parse_args()

# --Helpers-- #

def push_item_to_siem(_item, data_type):
    print(f'POST/PUT ({data_type}) record')

def push_data_to_siem(data, data_type):
    print(f'POST/PUT {len(data)} ({data_type}) records')

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

# Ranges

date_time_1    = datetime.datetime.now()
tz_date_time_1 = datetime.datetime.now(tz.tzlocal())

date_time_0 = date_time_1 - datetime.timedelta(hours = args.hours)
tz_date_time_0 = tz_date_time_1 - datetime.timedelta(hours = args.hours)

iso_date_time_0 = f"{date_time_0.isoformat(sep='T')}Z"
iso_date_time_1 = f"{date_time_1.isoformat(sep='T')}Z"

# Query

print('Query Period:')
print(f'    From: {date_time_0}')
print(f'    To:   {date_time_1}')
print()

audit_query_params = {
    'from':  iso_date_time_0,
    'to':    iso_date_time_1,
    'sort': 'time'
}

if args.no_core_audits:
    for audit_type in pc_api.compute_audit_types():
        audits = pc_api.audits_list_read(audit_type=audit_type, query_params=audit_query_params)
        push_data_to_siem(audits, data_type=audit_type)

if args.host_forensic_activities:
    audits = pc_api.host_forensic_activities_list_read(query_params=audit_query_params)
    push_data_to_siem(audits, data_type='forensic/activities')

log_query_params = {
    'lines': args.log_limit
}

if args.console_logs:
    print()
    print(f'Log Limit: {args.log_limit}')
    print()

    logs_in_scope = []
    logs = pc_api.console_logs_list_read(query_params=log_query_params)
    for log in logs:
        if log['time']:
            tz_log_time = parser.isoparse(log['time']).astimezone(tz.tzlocal())
            if tz_date_time_0 <= tz_log_time <= tz_date_time_1:
                logs_in_scope.append(log)
    push_data_to_siem(logs_in_scope, data_type='logs/console')
