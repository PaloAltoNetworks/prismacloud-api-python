
import requests
import json
import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta

#change everything up until /api before use to match your environment
# Navigate to Compute > Manage > System > Utilities and copy the value of Path to Console
url1 = "(your path to console here)/api/v1/authenticate"
url2 = "(your path to console here)/api/v1/audits/mgmt"

# variables to set date from search - I have this set to 1 month  
# to change this update the relativedelta months = to whatever you like
today = datetime.today()
startDate = today - relativedelta(months=1)
startDateFormatted = startDate.strftime("%Y-%m-%d")

#use your access key and secret key that you set up from the SaaS console 
payload = {
    "username": "(Access Key)",
    "password": "(Secret Key)"
}
headers1 = {"content-type": "application/json"}

response1 = requests.request("POST", url1, json=payload, headers=headers1)

jsonResponse = response1.json()
print(response1)

#stores JWT token for API call to audit logs
token = jsonResponse["token"]


# Pull audit log from the last 24 hours this is configurable: https://prisma.pan.dev/api/cloud/cspm/audit-logs#operation/rl-audit-logs
querystring = {"from": f"{startDateFormatted}"}

headers2 = {"content-type": "application/json", "Authorization": "Bearer %s" % (token)}

response2 = requests.request("GET", url2, headers=headers2, params=querystring)

print("audit logs")
auditLogsJson = response2.json()

#open file to write to
data_file = open('cwppAuditLog.csv', 'w')
# create the csv writer object
csv_writer = csv.writer(data_file)
# Counter variable used for writing
# headers to the CSV file
count = 0

print("Print each key-value pair from JSON response")
for item in auditLogsJson: 
    if count == 0:
            # Writing headers of CSV file
            header = item.keys()
            csv_writer.writerow(header)
            count += 1

    # Writing data of CSV file
    if item["type"] != "login":
        csv_writer.writerow(item.values())

data_file.close()               
 