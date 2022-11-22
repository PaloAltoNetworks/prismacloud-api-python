""" Get Outdated Defenders """

from packaging import version

from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--csv',
    action="store_true",
    help="(Optional) - save output to outdated_defenders.csv"
)
parser.add_argument(
    '--quiet',
    action="store_true",
    help="(Optional) - supress console output"
)
args = parser.parse_args()

# --Helpers-- #

def output(*a):
    if not args.quiet:
        print(*a)
    if args.csv:
        print(*a, file=csvoutfile)

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)
csvoutfile = None
if args.csv:
    csvoutfile = open("outdated_defenders.csv", "w")

# --Main-- #

# Note: default provider is aws
# To-do: support other cloud providers

current_version = pc_api.execute_compute('GET', 'api/v1/version')
output('Current console version: %s' % current_version)

defenders = pc_api.execute_compute('GET', 'api/v1/defenders')

output('Provider, Cloud Account, Region, Defender, Version, Type, Outdated')
for defender in defenders:
    outdated = version.parse(defender['version']) < version.parse(current_version)
    provider = "Unknown"
    account = "Unknown"
    region = "Unknown"
    if 'cloudMetadata' in defender:
        metadata = defender['cloudMetadata']
        if 'provider' in metadata:
            provider = metadata['provider']
        if 'accountID' in metadata:
            account = metadata['accountID']
        if 'region' in metadata:
            region = metadata['region']
    output('%s, %s, %s, %s, %s, %s, %s' % (provider, account, region, defender['hostname'], defender['version'], defender['type'], outdated))
