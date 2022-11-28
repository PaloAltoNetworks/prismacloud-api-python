""" Collect Compute Audits, History, and Logs """

# Use this script to forward Audits, and Console History and Logs from Prisma Cloud Compute to a SIEM.
# It is expected to be called once an hour, by default, to read from the Prisma Cloud API and write to your SIEM API.
# It depends upon the SIEM to deduplicate data, and requires you to modify the `send_data_to_siem()` function for your SIEM API.

import concurrent.futures
import json
import inspect
import time
import sys

from pathlib import Path
from typing import Union

import requests

from datetime import datetime, timedelta, timezone
from dateutil import parser, tz
 
# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

ENABLE_PROFILING = False
OUTER_CONCURRENY = 1
INNER_CONCURRENY = 1
OUTPUT_DIRECTORY = '/tmp/prisma-cloud-compute-data'

DEFAULT_HOURS = 1
DEFAULT_MINUTES_OVERLAP = 1
DEFAULT_CONSOLE_LOG_LIMIT = 32768

this_parser = pc_utility.get_arg_parser()
this_parser.add_argument(
    '--hours',
    type=int,
    default=DEFAULT_HOURS,
    help=f'(Optional) - Time period to collect, in hours, from now. (Default: {DEFAULT_HOURS})')
this_parser.add_argument(
    '--minutes_overlap',
    type=int,
    default=DEFAULT_MINUTES_OVERLAP,
    help=f'(Optional) - Minutes of overlap for time period to collect. (Default: {DEFAULT_MINUTES_OVERLAP})')
this_parser.add_argument(
    '--audit_events',
    action='store_true',
    help='(Optional) - Collect Audit Events. (Default: disabled)')
this_parser.add_argument(
    '--host_forensic_activities',
    action='store_true',
    help='(Optional) - Collect Host Forensic Activity. Warning: high-volume/time-intensive. (Default: disabled)')
this_parser.add_argument(
    '--console_history',
    action='store_true',
    help='(Optional) - Collect Console History. (Default: disabled)')
this_parser.add_argument(
    '--console_logs',
    action='store_true',
    help='(Optional) - Collect Console Logs. (Default: disabled)')
this_parser.add_argument(
    '--console_logs_limit',
    type=int,
    default=DEFAULT_CONSOLE_LOG_LIMIT,
    help=f'(Optional) - Number of messages to collect, requires --console_logs. (Default: {DEFAULT_CONSOLE_LOG_LIMIT})')
args = this_parser.parse_args()

# -- User Defined Functions-- #

def outbound_api_call(data_type:str, data: Union[list, dict]):
    # Transform data into the format expected by the request to your SIEM.
    data['event'] = data_type
    profile_log('OUTBOUND_API_CALL', 'STARTING')
    req_method       = 'POST'
    req_url          = ''
    req_headers      = {}
    req_query_params = {}
    req_body_params  = data
    req_timeout      = 4
    retry_status_codes = [401, 429, 500, 502, 503, 504]
    retry_limit = 4
    retry_pause = 8
    # Configure req_url to enable the request.
    if not req_url:
        print(f'        OUTBOUND_API_CALL for {data_type} STUB ...')
        profile_log('OUTBOUND_API_CALL', 'FINISHED')
        return
    print(f'        OUTBOUND_API_CALL for {data_type} ...')
    api_response = requests.request(req_method, req_url, headers=req_headers, params=req_query_params, data=json.dumps(req_body_params), timeout=req_timeout, verify=False)
    if api_response.status_code in retry_status_codes:
        for _ in range(1, retry_limit):
            time.sleep(retry_pause)
            api_response = requests.request(req_method, req_url, headers=req_headers, params=req_query_params, data=json.dumps(req_body_params), timeout=req_timeout, verify=False)
            if api_response.ok:
                break # break retry loop
    if not api_response.ok:
        print(f'API: {req_url} responded with an error: {api_response.status_code}')
    profile_log('OUTBOUND_API_CALL', 'FINISHED')

# --Functions-- #

def process_audit_events(audit_type: str, query_params: dict):
    audits = pc_api.audits_list_read(audit_type=audit_type, query_params=query_params)
    send_data_to_siem(data_type=audit_type, data=audits)

def process_host_forensic_activities(query_params: dict):
    audits = pc_api.host_forensic_activities_list_read(query_params=query_params)
    send_data_to_siem(data_type='forensic/activities', data=audits)

def process_console_history(query_params: dict):
    audits = pc_api.console_history_list_read(query_params=query_params)
    send_data_to_siem(data_type='audits/mgmt', data=audits)

def process_console_logs(query_params: dict, time_range: dict):
    matching_console_logs = []
    console_logs = pc_api.console_logs_list_read(query_params=query_params)
    for this_log in console_logs:
        if this_log['time']:
            log_datetime = parser.isoparse(this_log['time']).astimezone(tz.tzlocal())
            if time_range['from'] <= log_datetime <= time_range['to']:
                matching_console_logs.append(this_log)
    send_data_to_siem(data_type='logs/console', data=matching_console_logs)

####

def send_data_to_siem(data_type: str, data: list, send_as_list=False):
    profile_log(data_type, 'STARTING')
    print(f'    PROCESSING {len(data)} ({data_type}) records')
    if send_as_list:
        outbound_api_call(data_type, data)
    else:
        inner_futures = []
        with concurrent.futures.ThreadPoolExecutor(INNER_CONCURRENY) as inner_executor:
            for data_item in data:
                inner_futures.append(inner_executor.submit(
                        #outbound_api_call(data_type, data_item)
                        outbound_api_call, data_type, data_item
                    )
                )
            concurrent.futures.wait(inner_futures)
    profile_log(data_type, 'FINISHED')

####

def create_output_directory():
    Path(OUTPUT_DIRECTORY).mkdir(parents=True, exist_ok=True)

####

def profile_log(detail: str, state: str, initialize=False):
    if not ENABLE_PROFILING:
        return
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # To output profile_log specific to each execution, use:
    # log_file_name = '%s/%s_log.txt' % (OUTPUT_DIRECTORY, timestamp)
    log_file_name = '%s/log.txt' % OUTPUT_DIRECTORY
    if initialize:
        mode = 'w'
    else:
        mode = 'a'
    with open(log_file_name, mode) as log_file:
        entry = '%s\t%s\t%s\t%s\n' % (timestamp, state, inspect.stack()[1][3], detail)
        log_file.write(entry)

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

profile_log('Collect Compute Audits, History, and Logs', 'STARTING', True)

create_output_directory()

print('Collect Compute Audits, History, and Logs')
print()

# Dates

date_time_1 = datetime.now(timezone.utc).replace(microsecond=0)
date_time_0 = date_time_1 - timedelta(hours=args.hours, minutes=args.minutes_overlap)

datetime_range = {
    'from':  f"{date_time_0.isoformat()}Z".replace('+00:00Z', '.000Z'),
    'to':    f"{date_time_1.isoformat()}Z".replace('+00:00Z', '.000Z'),
    'sort': 'time'
}

console_logs_datetime_range = {
    'from':  date_time_0,
    'to':    date_time_1,
}

console_logs_query_params = {
    'lines': args.console_logs_limit
}

print('Query Period:')
print('    From: %s' % datetime_range['from'])
print('    To:   %s' % datetime_range['to'])
print()

# Calculon Compute!

outer_futures = []
with concurrent.futures.ThreadPoolExecutor(OUTER_CONCURRENY) as executor:

    if args.audit_events:
        print('Collecting Audits')
        print()
        for this_audit_type in pc_api.compute_audit_types():
            outer_futures.append(executor.submit(
                    # aka: process_audit_events(this_audit_type, datetime_range)
                    process_audit_events, this_audit_type, datetime_range
                )
            )
        concurrent.futures.wait(outer_futures)
        print()

    if args.host_forensic_activities:
        print('Collecting Host Forensic Activity Audits (high-volume/time-intensive, please wait)')
        print()
        outer_futures.append(executor.submit(
                # aka: process_host_forensic_activities(datetime_range)
                process_host_forensic_activities, datetime_range
            )
        )
        print()

    if args.console_history:
        print('Collecting Console History')
        print()
        outer_futures.append(executor.submit(
                # aka: process_console_history(datetime_range)
                process_console_history, datetime_range
            )
        )
        print()

    if args.console_logs:
        print(f'Collecting Console Logs (Limit: {args.console_logs_limit})')
        print()
        outer_futures.append(executor.submit(
                # aka: process_console_logs(console_logs_query_params, console_logs_datetime_range)
                process_console_logs, console_logs_query_params, console_logs_datetime_range
            )
        )
        print()
    concurrent.futures.wait(outer_futures)

profile_log('Collect Compute Audits, History, and Logs', 'FINISHED')

print('Done')
print()
