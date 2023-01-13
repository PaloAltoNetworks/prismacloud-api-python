""" Download and Save Forensics """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--workload_id',
    type=str,
    help='Workload ID.')
parser.add_argument(
    '--workload_type',
    type=str,
    choices=['host', 'container', 'app-embedded'],
    help='Workload Type.')
parser.add_argument(
    '--defender_hostname',
    type=str,
    help='Defender Hostname.')
parser.add_argument(
    '--file',
    type=str,
    help='Download forensics bundle to this file (extension auto-appended).'
)
args = parser.parse_args()

# --Initialize-- #

pc_api.configure(pc_utility.get_settings(args))

# --Main-- #

data = pc_api.forensic_read(workload_id=args.workload_id, workload_type=args.workload_type, defender_hostname=args.defender_hostname)

if args.workload_type == 'container':
    filename = "%s%s" % (args.file, '.tgz')
    with open(args.file, 'wb') as download:
        download.write(data)
    print('Downloaded forensics bundle to: %s' % filename)
else:
    filename = "%s%s" % (args.file, '.csv')
    with open(filename, 'w') as download:
        for item in data:
            download.write("%s\n" % item)
    print('Downloaded forensics to: %s' % filename)
