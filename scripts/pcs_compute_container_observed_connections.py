""" Get a list of vulnerable containers and their clusters """

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
    '--namespace',
    type=str,
    required=True,
    help='(Required) - Namespace.')
parser.add_argument(
    '-x',
    action='store_true',
    help='(Optional) - Exclude connections external to the specified namespace.')
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

print('Getting container connections for cluster: (%s) and namespace: (%s).' % (args.cluster, args.namespace))
if args.x:
    print('Excluding connections external to namespace.')
print()

connections = []
container_image_names = {}

radar = pc_api.execute_compute('GET', 'api/v1/radar/container?clusters=%s&namespaces=%s&project=Central+Console' % (args.cluster, args.namespace))
containers = radar['radar']

for container in containers:
    container_image_names[container['_id']] = container['imageNames'][0].rsplit('/', 1)[-1]

for container in containers:
    for incoming_connection in container['incomingConnections']:
        for port in incoming_connection['ports']:
            src_name = container_image_names.get(incoming_connection['profileID'], 'EXTERNAL TO NAMESPACE')
            if args.x and src_name == 'EXTERNAL TO NAMESPACE':
                continue
            connections.append({
                'dst_name': container_image_names[container['_id']],
                'dst_port': port['port'],
                'src_name': src_name,
            })

sorted_connections = sorted(connections, key=lambda d: (d['dst_name'], d['dst_port']))

for connection in sorted_connections:
    print(connection)
