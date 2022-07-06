
import requests
import json
import csv

url1 = "https://api3.prismacloud.io/login"
url2 = "https://api3.prismacloud.io/audit/redlock"


payload = {
    "password": "(access key)",
    "username": "(secret key)"
}
headers1 = {"content-type": "application/json; charset=UTF-8"}

response1 = requests.request("POST", url1, json=payload, headers=headers1)

jsonResponse = response1.json()

#stores JWT token for API call to audit logs
token = jsonResponse["token"]


# Pull audit log from the last 24 hours this is configurable: https://prisma.pan.dev/api/cloud/cspm/audit-logs#operation/rl-audit-logs
querystring = {"timeType":"relative","timeAmount":"1","timeUnit":"month"}

headers2 = {"x-redlock-auth": token}

response2 = requests.request("GET", url2, headers=headers2, params=querystring)

print("audit logs")
auditLogsJson = response2.json()

#open file to write to
data_file = open('cspmAuditLog.csv', 'w')
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
    if item["actionType"] != "LOGIN":
        csv_writer.writerow(item.values())

data_file.close()               
 