""" Triggers a registry scan and returns a file containing all the results from that scan """

# This provides a view of the current state of the registries
# (i.e. not including images that no longer exist in the registries).

import datetime
import time

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--registry',
    type=str,
    help='(Optional) - The scanned registry')
parser.add_argument(
    '--repository',
    type=str,
    help='(Optional) - The scanned repository')
parser.add_argument(
    '--tag',
    type=str,
    help='(Optional) - The scanned tag')
args = parser.parse_args()

# --Helpers-- #

def registry_scan_wait():
    registry_scan_idle = False
    while registry_scan_idle is False:
        registry_status = pc_api.statuses_registry()
        if registry_status and registry_status.get('completed', False) is True:
            registry_scan_idle = True
        else:
            print('.')
            time.sleep(4)

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)
pc_api.validate_api_compute()

registry_params = None
if args.registry or args.repository or args.repository:
    registry_params = {
        'registry':   args.registry,
        'repository': args.repository,
        'tag':        args.tag
    }

OUTPUT_FILE='current_registry_results.json'

# --Main-- #

print('Testing Compute API Access ...', end='')
intelligence = pc_api.statuses_intelligence()
print(' done.')
print()

print('Waiting until any already-running registry scan has completed ...')
registry_scan_wait()
print('Done.')
print()

now = datetime.datetime.now()
print('Scanning registry starting at %s ...' % now.strftime("%Y-%m-%d %H:%M:%S"), end='')
pc_api.registry_scan(body_params=registry_params)
print(' done.')
print()

print('Waiting until the current running registry scan has completed ...')
registry_scan_wait()
print('Done.')
print()

registry_list = pc_api.registry_list_read()

pc_utility.write_json_file(OUTPUT_FILE, registry_list, pretty=True)
print('Registry scan data written to: %s' % OUTPUT_FILE)
print()
