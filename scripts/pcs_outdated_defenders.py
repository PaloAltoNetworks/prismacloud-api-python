""" Get Outdated Defenders """

from packaging import version

from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--csv',
    action="store_true",
    help="(Optional) - Save output to 'outdated_defenders.csv'"
)
parser.add_argument(
    '--quiet',
    action="store_true",
    help="(Optional) - Supress console output"
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
pc_api.validate_api_compute()

# --Main-- #

# Note: Default provider is AWS.
# To-Do: Support other cloud providers

csvoutfile = None

if args.csv:
    csvoutfile = open('outdated_defenders.csv', 'w')

current_version = pc_api.execute_compute('GET', 'api/v1/version')

output('Current Console Version: %s' % current_version)

defenders = pc_api.execute_compute('GET', 'api/v1/defenders')

output('Provider, Cloud Account, Region, Defender, Version, Type, Outdated')

for defender in defenders:
    outdated = version.parse(defender['version']) < version.parse(current_version)
    provider = defender.get('provider', 'Unknown')
    account  = defender.get('accountID', 'Unknown')
    region   = defender.get('region', 'Unknown')
    metadata = defender.get('cloudMetadata', 'Unknown')
    output('%s, %s, %s, %s, %s, %s, %s' % (provider, account, region, defender['hostname'], defender['version'], defender['type'], outdated))
