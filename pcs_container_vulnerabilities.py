""" Get Vulnerabilities in Containers (Deployed Images) """

from __future__ import print_function
from pc_lib import pc_api, pc_utility

import json

# --Configuration-- #

parser = pc_utility.get_arg_parser()

parser.add_argument('-d', '--debug',
    action='store_true',
    help='(Optional) Enable debugging.')

args = parser.parse_args()

DEBUG_MODE = args.debug

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

# Monitor > Vulnerabilities/Compliance > Images > Deployed

print('Getting Vulnerabilities in Containers (Deployed Images) ...')
print()

print('Image Name\tContainers\tContainers\tHosts\tVulnerability Count')

images = pc_api.images_list_read()
for image in images:
    if DEBUG_MODE:
        print(json.dumps(image, indent=4))
    image_id = image['_id']
    vulnerabilities = image['vulnerabilities']

    containers = pc_api.containers_list_read(image_id)
    container_names = []
    container_host_names = []
    for container in containers:
        if DEBUG_MODE:
            print(json.dumps(container, indent=4))
        image_name = container['info']['imageName']
        container_names.append(container['info']['name'])
        container_host_names.append(container['hostname'])

    container_names.sort()
    container_host_names.sort()

    print('%s\t%s\t%s\t%s' % (image_name, container_names, container_host_names, len(vulnerabilities)))

print()
print('Done.')
print()
