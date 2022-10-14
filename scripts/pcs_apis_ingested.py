""" Get a list of Alerts """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

clouds = ['alibaba-', 'aws-', 'azure-', 'gcloud-', 'gcp-', 'oci-']
apis = []

for cloud in clouds:
    query = {}
    query['query'] = "config from cloud.resource where api.name = '%s" % cloud
    query['cursor'] = len(query['query'])
    result = pc_api.search_suggest_list_read(query_to_suggest=query)
    if 'suggestions' in result:
        suggestions = result['suggestions']
        single = [s.replace("'", '') for s in suggestions]
        double = [s.replace('"', '') for s in single]
        apis.extend(double)

apis.sort()
for api in apis:
    print(api)
