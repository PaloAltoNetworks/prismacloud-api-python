""" Get a list of vulnerable containers and their clusters """

import urllib.parse

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--cluster',
    type=str,
    required=True,
    help='(Required) - Cluster.')
parser.add_argument(
    '--collection',
    type=str,
    help='(Optional) - Collection.')
parser.add_argument(
    '--namespace',
    type=str,
    help='(Optional) - Namespace.')
parser.add_argument(
    '-x',
    action='store_true',
    help='(Optional) - Exclude connections external to the specified collection and/or namespace.')
args = parser.parse_args()

# --Helpers-- #

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)
pc_api.validate_api_compute()

# --Main-- #

print('Testing Compute API Access ...', end='')
intelligence = pc_api.statuses_intelligence()
print(' done.')
print()

print('Getting container connections for Cluster: (%s) Collection: (%s) Namespace: (%s).' % (args.cluster, args.collection, args.namespace))
if args.x:
    print('Excluding connections external to the specified collection and/or namespace.')
print()

# Define variables.

connections = []
containers = {}

# Note: the cluster, collection, and namespace script arguments are singletons,
# but could be comma-delimited arrays, as the endpoint parameters accept arrays.

if ',' in args.cluster:
    pc_utility.error_and_exit(400, 'This script is arbitrarily limited to querying one cluster')

cluster = urllib.parse.quote(args.cluster)

if args.collection:
    collection = '&collections=%s' % urllib.parse.quote(args.collection)
else:
    collection = ''

if args.namespace:
    namespace = '&namespaces=%s' % urllib.parse.quote(args.namespace)
else:
    namespace = ''

# Query the endpoint.

radar = pc_api.execute_compute('GET', 'api/v1/radar/container?project=Central+Console&clusters=%s%s%s' % (cluster, collection, namespace))
if not radar or not radar['radar']:
    pc_utility.error_and_exit(400, 'No containers match the specified parameters.')
radar_containers = radar['radar']

# Convert the list of container dictionaries into a dictionary of container dictionaries.

for container in radar_containers:
    containers[container['_id']] = container

# Convert containers into a list of connection dictionaries.

for radar_container in radar_containers:
    for incoming_connection in radar_container['incomingConnections']:
        for port in incoming_connection['ports']:
            src_container = containers.get(incoming_connection['profileID'])
            if src_container:
                src_name = src_container['imageNames'][0].rsplit('/', 1)[-1]
                src_namespace = src_container['namespace']
            else:
                if args.x:
                    # Exclude connections external to the specified collection and/or namespace.
                    continue
                src_name = 'EXTERNAL TO QUERY'
                src_namespace = 'EXTERNAL TO QUERY'
            connections.append({
                'dst_name': radar_container['imageNames'][0].rsplit('/', 1)[-1],
                'dst_port': port['port'],
                'dst_namespace': radar_container['namespace'],
                'src_name': src_name,
                'src_namespace': src_namespace
            })

# Output the list of connection dictionaries.

sorted_connections = sorted(connections, key=lambda d: (d['dst_name'], d['dst_port']))

for connection in sorted_connections:
    print(connection)
