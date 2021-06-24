""" Get Vulnerabilities in Containers (Deployed Images) """

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

vulnerabilities_by_container = []

print('Getting Deployed Images (please wait) ...', end='')
images = pc_api.images_list_read()
print(' done.')
print()

print('Getting Containers (please wait) ...', end='')
containers = pc_api.containers_list_read()
print(' done.')
print()

#containers_dictionary = {}
#for container in containers:
#   containers_dictionary[container['_id']] = container
   
for image in images:
    if image['instances'][0]['image'] != 'argoproj/argocd:v1.8.7':
        continue
    if DEBUG_MODE:
        print(json.dumps(image, indent=4))
    image_id = image['_id']
    image_name = image['instances'][0]['image']
    if image['vulnerabilities']:
        vulnerabilities = image['vulnerabilities']
    else:
        vulnerabilities = []
    for container in containers:
        if DEBUG_MODE:
            print(json.dumps(container, indent=4))
        if 'imageID' in container['info'] and container['info']['imageID'] == image_id:
            image_name = container['info']['imageName']
            vulnerabilities_by_container.append({'name': container['info']['name'], 'host': container['hostname'], 'image': image_name, 'vulnerabilities': vulnerabilities})

print('Container Name\tHost Name\tImage Name\tVulnerability Count')
for container in vulnerabilities_by_container:
    print('%s\t%s\t%s\t%s' % (container['name'], container['host'], container['image'], len(container['vulnerabilities'])))
print()
