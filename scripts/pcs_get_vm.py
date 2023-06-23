""" Get a list of Alerts """

import json
import pandas as pd
from datetime import date
from tabulate import tabulate

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
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

search_params = {}
search_params['limit'] = 100
search_params['timeRange'] = {}
search_params['timeRange']['type']            = 'relative'
search_params['timeRange']['value']           = {}
search_params['timeRange']['value']['unit']   = 'day'
search_params['timeRange']['value']['amount'] = args.timerange
search_params['withResourceJson'] = False
search_params['query'] = 'config from cloud.resource where api.name = "azure-vm-list" AND resource.status = Active addcolumn [\'properties.networkProfile\'].networkInterfaces[*].ipConfigurations[*].publicIpAddress [\'properties.networkProfile\'].networkInterfaces[*].ipConfigurations[*].privateIpAddress'

print('API - Getting the RQL results ...', end='')
result_list = pc_api.search_config_read(search_params=search_params)
print()

print('Results:')
# print(json.dumps(result_list))
print()

pd_object = pd.read_json(json.dumps(result_list))
df = pd.DataFrame(pd_object)
output_azure = df[["cloudType","name","accountId","regionName","insertTs","deleted","dynamicData"]]
#output = df[["cloudType","name","accountId","regionName","insertTs","deleted"]]
output_azure['insertTs'] = output_azure['insertTs'].apply(lambda x: (pd.Timestamp(x*1000*1000)).strftime('%Y-%m-%d'))

#output = df[["cloudType","name","accountId","regionName","deleted"]]
#print(tabulate(output, headers = 'keys', tablefmt = 'psql'))
#print(tabulate(df, headers = 'keys', tablefmt = 'psql'))

#print('Result Count:')
#print(len(result_list))

# python3 ./pcs_rql_query_vm.py 'config from cloud.resource where api.name = "aws-ec2-describe-instances" AND resource.status = Active addcolumn privateIpAddress publicIpAddress'

search_params['query'] = 'config from cloud.resource where api.name = "aws-ec2-describe-instances" AND resource.status = Active addcolumn privateIpAddress publicIpAddress'

print('API - Getting the RQL results ...', end='')
result_list = pc_api.search_config_read(search_params=search_params)
print(' done.')
print()

print('Results:')
# print(json.dumps(result_list))
print()

pd_object = pd.read_json(json.dumps(result_list))
df = pd.DataFrame(pd_object)
output_aws = df[["cloudType","name","accountId","regionName","insertTs","deleted","dynamicData"]]
output_aws['insertTs'] = output_aws['insertTs'].apply(lambda x: (pd.Timestamp(x*1000*1000)).strftime('%Y-%m-%d'))

#output = df[["cloudType","name","accountId","regionName","deleted"]]
#print(tabulate(output, headers = 'keys', tablefmt = 'psql'))
#print(tabulate(df, headers = 'keys', tablefmt = 'psql'))

#print('Result Count:')
#print(len(result_list))

# python3 ./pcs_rql_query_vm.py 'config from cloud.resource where api.name = "aws-ec2-describe-instances" AND resource.status = Active addcolumn privateIpAddress publicIpAddress'

search_params['query'] = 'config from cloud.resource where api.name = "gcloud-compute-instances-list" addcolumn $.networkInterfaces[*].networkIP networkInterfaces[*].accessConfigs[*].natIP '

print('API - Getting the RQL results ...', end='')
result_list = pc_api.search_config_read(search_params=search_params)
print()

print('Results:')
# print(json.dumps(result_list))
print()

pd_object = pd.read_json(json.dumps(result_list))
df = pd.DataFrame(pd_object)
output_gcp = df[["cloudType","name","accountId","regionName","insertTs","deleted","dynamicData"]]
#output = df[["cloudType","name","accountId","regionName","insertTs","deleted"]]
output_gcp['insertTs'] = output_gcp['insertTs'].apply(lambda x: (pd.Timestamp(x*1000*1000)).strftime('%Y-%m-%d'))

search_params['query'] = 'config from cloud.resource where api.name = "oci-compute-instance" and resource.status = Active '

print('API - Getting the RQL results ...', end='')
result_list = pc_api.search_config_read(search_params=search_params)
print()

print('Results:')
# print(json.dumps(result_list))
print()

pd_object = pd.read_json(json.dumps(result_list))
df = pd.DataFrame(pd_object)
output_oci = df[["cloudType","name","accountId","regionName","insertTs","deleted"]]
#output = df[["cloudType","name","accountId","regionName","insertTs","deleted"]]
output_oci['insertTs'] = output_oci['insertTs'].apply(lambda x: (pd.Timestamp(x*1000*1000)).strftime('%Y-%m-%d'))



result = pd.concat([output_azure, output_aws, output_gcp, output_oci],ignore_index=True)
#output = df[["cloudType","name","accountId","regionName","deleted"]]
print(tabulate(result, headers = 'keys', tablefmt = 'psql'))
#print(tabulate(df, headers = 'keys', tablefmt = 'psql'))

#print('Result Count:')
#print(len(result_list))

# python3 ./pcs_rql_query_vm.py 'config from cloud.resource where api.name = "aws-ec2-describe-instances" AND resource.status = Active addcolumn privateIpAddress publicIpAddress'
