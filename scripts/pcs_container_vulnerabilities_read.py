""" Get Vulnerabilities in Containers (Deployed Images) """

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

print('Getting Deployed Images (please wait) ...', end='')
images = pc_api.images_list_read(query_params={'filterBaseImage': 'true'})
print(' done.')
print()

print('Getting Containers (please wait) ...', end='')
containers = pc_api.containers_list_read()
print(' done.')
print()

images_dictionary = {}
for image in images:
    if pc_api.debug:
        print(json.dumps(image, indent=4))
    image_id = image['_id']
    images_dictionary[image_id] = image

for container in containers:
    if pc_api.debug:
        print(json.dumps(container, indent=4))
    if 'imageID' in container['info']:
        image_id   = container['info']['imageID']
        image_name = container['info']['imageName']
        if image_id in images_dictionary:
            if 'vulnerabilities' in images_dictionary[image_id] and images_dictionary[image_id]['vulnerabilities']:
                vulnerabilities = images_dictionary[image_id]['vulnerabilities']
            else:
                vulnerabilities = []
        else:
            vulnerabilities = []
        vulnerabilities_by_container.append({'name': container['info']['name'], 'host': container['hostname'], 'image': image_name, 'vulnerabilities': vulnerabilities})

print('Container Name\tHost Name\tImage Name\tVulnerability Count')
for container in vulnerabilities_by_container:
    print('%s\t%s\t%s\t%s' % (container['name'], container['host'], container['image'], len(container['vulnerabilities'])))
print()
