""" Get Resources """

# pylint: disable=import-error
from prismacloudapi import pc_api, pc_utility
from tabulate import tabulate

import pandas as pd
import time
import datetime
import string
import random
import os

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    'week',
    type=int,
    help="number of week before today")
args = parser.parse_args()

# --Initialize-- #

# pc_utility.prompt_for_verification_to_continue(args)
settings = pc_utility.get_settings(args)
pc_api.configure(settings)

dt = datetime.datetime(year=2022, month=1, day=1)
data = ['critical', 'high', 'medium', 'low', 'information']
df_trend = pd.DataFrame(data, columns = ['Policy Severity'])
start_ts = time.mktime(dt.timetuple())*1000

# initializing size of string
N = 5
 
# using random.choices()
# generating random strings
res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

for x in range(args.week):
    end_ts = time.mktime((datetime.datetime.today() - datetime.timedelta(weeks = x)).timetuple())*1000
    print('API - Gernerate new CSV Report ...', end='')
    body_params = {
        "detailed": True,
        "fields":[
            "alert.id",
            "alert.status",
            "alert.time",
            "cloud.account",
            "cloud.accountId",
            "cloud.region",
            "resource.id",
            "resource.name",
            "policy.name",
            "policy.type",
            "policy.severity"
        ],
        "filters":[
            {"name":"policy.severity", "operator":"=", "value": "high"},
            {"name":"policy.severity", "operator":"=", "value": "critical"},
            {"name":"policy.severity", "operator":"=", "value": "medium"},
            {"name":"policy.severity", "operator":"=", "value": "low"},
            {"name":"alert.status","operator":"=", "value": "open"}
        ],
        "groupBy": [
            "cloud.account"
        ],
        "limit": 2000,
        "offset": 0,
        "sortBy": [
            "cloud.account"
        ],
        "timeRange": {
        "type": "absolute",
        "value": {
            "startTime": start_ts,
            "endTime": end_ts
            }
        }
    }

    print()
    print('Creating the Alert Report...', end='')
    print()
    alert_report = pc_api.alert_csv_create(body_params)
    print('Report Created with Report ID: %s' % alert_report['id'])
    report_time = time.strftime("%Y%m%d")
    report_filename = "./customer-report-" + report_time + "-" + res + "-" + str(x) + ".csv"
    column_name = str(x) + ' Week ago'
    print()

    report_ready = False
    report_dir = '.'

    while(not report_ready):
        alert_report_update = pc_api.alert_csv_status(alert_report['id'])
        # print('Getting the Alert Report Status...', alert_report_update['status'])
        time.sleep(2.5)    
        if (alert_report_update['status'] == 'READY_TO_DOWNLOAD'):
            csv_report = pc_api.alert_csv_download(alert_report['id'])
            # Write Download Report File to Current Report Directory
            file = open(report_filename, "w")
            file.write(csv_report)
            file.close()
            # print("Alert Report Downloaded...")
            break

    df = pd.read_csv(report_filename, usecols=['Policy Severity'])
    df_severity = df.groupby(['Policy Severity'])['Policy Severity'].count().to_frame()
    df_severity.columns = [column_name]
    df_severity = df_severity.reset_index()
    # df_trend = df_trend.merge(df_severity,left_on='Policy Severity',right_on='Policy Severity')
    df_trend = df_trend.merge(df_severity, on='Policy Severity', how='left')
    df_trend[column_name].fillna(0, inplace=True)
    os.remove(report_filename)

df_trend = df_trend.set_index('Policy Severity').transpose()
print(tabulate(df_trend, headers='keys', tablefmt='psql'))