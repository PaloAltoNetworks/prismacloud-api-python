""" Get Usage """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--cloud_account_group_name',
    type=str,
    help='Name of the Cloud Account Group to inspect.')
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

print('API - Getting the current list of Cloud Account Groups ...', end='')
cloud_account_groups_list = pc_api.cloud_account_group_list_read()
print(' done.')
print()

cloud_account_group = None
for item in cloud_account_groups_list:
    if item['name'] == args.cloud_account_group_name:
        cloud_account_group = item
        break

if not cloud_account_group:
    pc_utility.error_and_exit(400, "Cloud Account Group (%s) not found." % args.cloud_account_group_name)

if not cloud_account_group['accounts']:
    pc_utility.error_and_exit(400, "No Cloud Accounts in Account Group Group (%s)." % cloud_account_group['name'])

cloud_account_ids = [cloud_account['id'] for cloud_account in cloud_account_group['accounts']]
body_params = {
    'accountIds': cloud_account_ids,
    'timeRange': {'type':'relative', 'value': {'unit': 'month', 'amount': 1}}
}

print('API - Getting the Usage for Cloud Account Group (%s) ...' % cloud_account_group['name'], end='')
cloud_account_usage = pc_api.resource_usage_over_time(body_params=body_params)
print(' done.')
print()

# Example (dataPoints.counts) response from the API.

"""
{
    'alibaba_cloud': {
        'alibaba_ecs_instance': 0
    },
	'aws': {
		'aws_lb': 0,
		'rds': 0,
		'nat_gateway': 0,
		'redshift': 0,
		'iam': 0,
		'ec2_instance': 0
	},
    'azure': {
        'azure_vm': 0,
        'azure_lb': 0,
        'azure_postgresql_server': 0,
        'azure_sql': 0,
        'azure_sql_managed_instance': 0,
        'azure_iam': 0
    },
	'gcp': {
		'cloudsql': 0,
		'gcp_cloud_load_balancing_backend_service': 0,
		'gce_instance': 0,
		'gcp_compute_nat': 0
	},
	'oci': {
		'oci_compute_instance': 0
	},
	'others': {
		'container': 0,
		'host': 0,
		'serverless': 0,
		'waas': 0
	}
}
"""

# Note:
# It appears the API does not return values for all cloud types when 'cloudType' is not specified as a body parameter.
# We may have to loop through the cloud types and query each of them explicitly.

clouds = cloud_account_usage['dataPoints'][0]['counts'].keys()

for data_points in cloud_account_usage['dataPoints']:
    print(data_points['counts'])
    print()
