""" Download and Save Agentless Logs """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

DEFAULT_FILENAME = '/tmp/agentless_logs.tgz'

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--file',
    type=str,
    default=DEFAULT_FILENAME,
    help='Download agentless logs to this file. Default: %s' % DEFAULT_FILENAME
)
args = parser.parse_args()

# --Initialize-- #

pc_api.configure(pc_utility.get_settings(args))

# --Main-- #

data = pc_api.agentless_logs_list_read()

with open(args.file, 'wb') as download:
    download.write(data)

print('Downloaded agentless logs to: %s' % args.file)