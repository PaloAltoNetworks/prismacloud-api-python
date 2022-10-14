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

# Write a header and an array of data to a CSV file.

def write_file(file_name, header, data):
    with open(file_name, 'w') as data_file:
        data_file.write('%s\n' % header)
        data_file.write('\n'.join(data))

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

# https://prisma.pan.dev/api/cloud/cwpp/hosts#operation/get-hosts
print('Getting Hosts (please wait) ...', end='')
hosts = pc_api.hosts_list_read()
print(' done.')
print()

# https://prisma.pan.dev/api/cloud/cwpp/images#operation/get-images
print('Getting Deployed Images (please wait) ...', end='')
images = pc_api.images_list_read(query_params={'filterBaseImage': 'true'})
print(' done.')
print()

# https://prisma.pan.dev/api/cloud/cwpp/containers#operation/get-containers
print('Getting Containers (please wait) ...', end='')
containers = pc_api.containers_list_read()
print(' done.')
print()

hosts_dictionary = {}
for host in hosts:
    if pc_api.debug:
        print("#########################################################################")
        print(json.dumps(host, indent=4))
    hosts_id = host['_id']
    hosts_dictionary[hosts_id] = host

images_dictionary = {}
for image in images:
    if pc_api.debug:
        print("#########################################################################")
        print(json.dumps(image, indent=4))
    image_id = image['_id']
    images_dictionary[image_id] = image

for container in containers:
    if pc_api.debug:
        print("#########################################################################")
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
        # TODO:
        # if unique_host_of_this_container['stopped'] == False:
        #     vulnerabilities_by_container_on_running_hosts.append( ...
        vulnerabilities_by_container.append({'name': container['info']['name'], 'host': container['hostname'], 'image': image_name, 'vulnerabilities': vulnerabilities})

print('Container Name\tHost Name\tImage Name\tVulnerability Count')
for container in vulnerabilities_by_container:
    print('%s\t%s\t%s\t%s' % (container['name'], container['host'], container['image'], len(container['vulnerabilities'])))
print()

# TODO: Output:
# csv_header = ["Registry","Repository","Tag","Id","Distro","Hosts","Layer","CVE ID","Compliance ID","Type","Severity","Packages","Source Package","Package Version","Package License","CVSS","Fix Status","Fix Date","Grace Days","Risk Factors","Vulnerability Tags","Description","Cause","Containers","Custom Labels","Published","Discovered","Binaries","Clusters","Namespaces","Collections","Digest","Vulnerability Link","Apps","Package Path"]
# write_file('ci.csv', csv_header, vulnerabilities_by_container)
