""" Get Resources """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility
import pandas as pd
import time
import datetime
import json

# --Configuration-- #

parser = pc_utility.get_arg_parser()
args = parser.parse_args()

# --Initialize-- #

# pc_utility.prompt_for_verification_to_continue(args)
settings = pc_utility.get_settings(args)
pc_api.configure(settings)

dt = datetime.datetime(year=2022, month=1, day=1)
start_ts = time.mktime(dt.timetuple())*1000
end_ts = time.time()*1000
#dt = datetime.datetime(year=2023, month=1, day=31)
#end_ts = time.mktime(dt.timetuple())*1000

# --Main-- #

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
        {"name":"alert.status","operator":"=", "value": "open"}
    ],
    "groupBy": [
        "cloud.account"
    ],
    "limit": 1000,
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

print(body_params)

print()
print('Creating the Alert Report...', end='')
print()
alert_report = pc_api.alert_csv_create(body_params)
print('Report Created with Report ID: %s' % alert_report['id'])
report_time = time.strftime("%Y%m%d-%H%M%S")
report_filename = "./Reports/wistron-report-" + report_time + ".csv"
print()

report_ready = False
report_dir = './Reports'
info_dir = './Reports/Info'
info_filename = info_dir + '/' + 'wistron-info.csv'

while(not report_ready):
    alert_report_update = pc_api.alert_csv_status(alert_report['id'])
    print('Getting the Alert Report Status...', alert_report_update['status'])
    time.sleep(2.5)    
    if (alert_report_update['status'] == 'READY_TO_DOWNLOAD'):
        csv_report = pc_api.alert_csv_download(alert_report['id'])

        # Write Download Report File to Current Report Directory
        file = open(report_filename, "w")
        file.write(csv_report)
        file.close()
        print("Alert Report Downloaded...")
        break

print("Generating report with Wistron Information...")
report_csv = pd.read_csv(report_filename)
report_csv.head()

info_csv = pd.read_csv(info_filename)
info_csv.head()

inner_join = pd.merge(report_csv, 
    info_csv, 
    on ='Cloud Account Id', 
    how ='left')
df = pd.DataFrame(inner_join)

# exporting to Excel

output_filename = report_dir + '/wistron-merged-report-' + report_time + '.xlsx'
writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')
df.to_excel(writer,index = False, header=True, sheet_name='Alert Summary')

workbook  = writer.book
worksheet = writer.sheets['Alert Summary']

cell_format = workbook.add_format()
cell_format.set_text_wrap()
cell_format.set_bottom_color('#2986cc')

header_format = workbook.add_format()
header_format.set_text_wrap()
header_format.set_font_color('white')
header_format.set_bg_color('#2986cc')

worksheet.set_default_row(30, cell_format)
worksheet.set_row(0, 15)
worksheet.set_column(0, 23, 15, cell_format)
worksheet.set_column(1, 1, 50, cell_format)
worksheet.set_column(3, 3, 80, cell_format)
worksheet.set_column(6, 6, 25, cell_format)
worksheet.set_column(8, 9, 40, cell_format)
worksheet.set_column(10, 10, 25, cell_format)
worksheet.set_column(11, 11, 80, cell_format)
worksheet.set_column(13, 13, 30, cell_format)
worksheet.set_column(21, 21, 30, cell_format)
worksheet.set_column(23, 23, 30, cell_format)

writer.close()
