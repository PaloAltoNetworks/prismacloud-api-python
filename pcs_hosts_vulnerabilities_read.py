""" Get Vulnerabilities in Hosts (Running Hosts) """

import json

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
args = parser.parse_args()

# --Helpers-- #

def optional_print(txt='', mode=True):
    if mode:
        print(txt)

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)
pc_api.validate_api_compute()

# --Main-- #

print('Testing Compute API Access ...', end='')
intelligence = pc_api.statuses_intelligence()
print(' done.')
print()

vulnerabilities_by_container = []

print('Getting Hosts (please wait) ...', end='')
hosts = pc_api.hosts_list_read()
print(' done.')
print()

for host in hosts:
    if pc_api.debug:
        print(json.dumps(host, indent=4))
    host_id = "%s %s" % (host['_id'], host['hostname'])
    vulnerabilities = host['vulnerabilities']
    print('Host: %s' % host_id)
    if not vulnerabilities:
        continue
    for vulnerability in sorted(vulnerabilities, key=lambda v: v['cve']):
        print('    %s (%s)' % (vulnerability['cve'], vulnerability['vecStr']))
print()
