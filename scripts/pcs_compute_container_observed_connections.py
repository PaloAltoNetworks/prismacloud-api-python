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

connections = []
container_image_names = {}

# Note: the cluster, collection, and namespace script arguments are singletons, 
# but could be comma-delimited arrays, as the endpoint parameters accept arrays.

if ',' in args.cluster:
    pc_utility.error_and_exit(400, 'This script is arbitrarily limited to querying one cluster')
if args.collection and ',' in args.collection:
    pc_utility.error_and_exit(400, 'This script is arbitrarily limited to querying one collection')
if args.namespace and ',' in args.namespace:
    pc_utility.error_and_exit(400, 'This script is arbitrarily limited to querying one namespace')

cluster = urllib.parse.quote(args.cluster)

if args.collection:
   collection = '&collections=%s' % urllib.parse.quote(args.collection)
else:
   collection = ''
    
if args.namespace:
   namespace = '&namespaces=%s' % urllib.parse.quote(args.namespace)
else:
   namespace = ''
    
radar = pc_api.execute_compute('GET', 'api/v1/radar/container?project=Central+Console&clusters=%s%s%s' % (cluster, collection, namespace))

containers = radar['radar']

# print
# print(containers)
# print

for container in containers:
    container_image_names[container['_id']] = container['imageNames'][0].rsplit('/', 1)[-1]

for container in containers:
    for incoming_connection in container['incomingConnections']:
        for port in incoming_connection['ports']:
            src_name = container_image_names.get(incoming_connection['profileID'], 'EXTERNAL TO QUERY')
            if args.x and src_name == 'EXTERNAL TO QUERY':
                continue
            connections.append({
                'dst_name': container_image_names[container['_id']],
                'dst_port': port['port'],
                'src_name': src_name,
                'namespace': container['namespace']
            })

sorted_connections = sorted(connections, key=lambda d: (d['dst_name'], d['dst_port']))

for connection in sorted_connections:
    print(connection)
