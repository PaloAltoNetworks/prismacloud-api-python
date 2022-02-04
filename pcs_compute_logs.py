""" Collect Compute Audits, History, and Logs """

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
    '--no_audit_events',
    action='store_true',
    help='(Optional) - Do not collect Audit Events. (Default: disabled)')
this_parser.add_argument(
    '--host_forensic_activities',
    action='store_true',
    help='(Optional) - Collect Host Forensic Activity. Warning: potentially high volume. (Default: disabled)')
this_parser.add_argument(
    '--console_history',
    action='store_true',
    help='(Optional) - Collect Console History. (Default: disabled)')
this_parser.add_argument(
    '--console_logs',
    action='store_true',
    help='(Optional) - Collect Console Logs. (Default: disabled)')
this_parser.add_argument(
    '--console_log_limit',
    type=int,
    default=32768,
    help='(Optional) - Number of console logs to collect, requires --console_logs. (Default: 32768)')
args = this_parser.parse_args()

# --Helpers-- #

def send_item_to_siem(_item, data_type):
    print(f'    PUT ({data_type}) record')

def send_data_to_siem(data, data_type):
    print(f'    PUT {len(data)} ({data_type}) records')

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

print('Collect Compute Audits, History, and Logs')
print()

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

if not args.no_audit_events:
    print('Collect Audits')
    print()
    for audit_type in pc_api.compute_audit_types():
        audits = pc_api.audits_list_read(audit_type=audit_type, query_params=audit_query_params)
        send_data_to_siem(audits, data_type=audit_type)
    print()

if args.host_forensic_activities:
    print('Collect Host Forensic Activity Audits (potentially high-volume, please wait)')
    print()
    audits = pc_api.host_forensic_activities_list_read(query_params=audit_query_params)
    send_data_to_siem(audits, data_type='forensic/activities')
    print()

if args.console_history:
    print('Collect Console History')
    print()
    audits = pc_api.console_history_list_read(query_params=audit_query_params)
    send_data_to_siem(audits, data_type='audits/mgmt')
    print()

console_log_query_params = {
    'lines': args.console_log_limit
}

if args.console_logs:
    print('Collect Console History')
    print()
    print('Console Log Limit:')
    print(f'    {args.console_log_limit}')
    print()

    logs_in_scope = []
    logs = pc_api.console_logs_list_read(query_params=console_log_query_params)
    for log in logs:
        if log['time']:
            tz_log_time = parser.isoparse(log['time']).astimezone(tz.tzlocal())
            if tz_date_time_0 <= tz_log_time <= tz_date_time_1:
                logs_in_scope.append(log)
    send_data_to_siem(logs_in_scope, data_type='logs/console')
