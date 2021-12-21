""" Get a list of vulnerable containers and their clusters """

from __future__ import print_function
from pc_lib import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--mode',
    type=str,
    choices=['registry', 'deployed', 'all'],
    default='all',
    help='(Optional) - Report on CI, Registry, Deployed, or all Images.')
parser.add_argument(
    '--cve',
    type=str,
    help='(Optional) - CVE to filter on.')
parser.add_argument(
    '--image_id',
    type=str,
    help='(Optional) - ID of the Image (sha256:...).')
args = parser.parse_args()

search_package_name    = None
search_package_version = None

# --Helpers-- #

def optional_print(txt='', mode=True):
    if mode:
        print(txt)

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)
pc_api.validate_api_compute()

# --Main-- #

get_ci_images       = True
get_registry_images = True
get_deployed_images = True

ci_images_with_package       = []
registry_images_with_package = []
deployed_images_with_package = []

print('Testing Compute API Access ...', end='')
intelligence = pc_api.statuses_intelligence()
print(' done.')
print()
# Monitor > Vulnerabilities/Compliance > Images > Registries
registry_images = {}
if args.mode in ['registry', 'all']:
    print('Getting Registry Images ...')
    images = pc_api.registry_list_read(args.image_id)
    optional_print(str(len(images))+' images total')
    for image in images:
        image_id = image['_id']
        vulns = image['vulnerabilities']
        if not vulns:
#            optional_print('No vulns for '+image_id)
            continue
        keep = False
        for vuln in vulns:
            if vuln['cve'] == args.cve:
                keep = True
                optional_print('Image '+image_id+' is vulnerable to '+args.cve)
                break
        if not keep:
#        optional_print('Excluding '+image_id)
            continue
# Monitor > Vulnerabilities/Compliance > Images > Deployed
deployed_images = {}
if args.mode in ['deployed', 'all']:
    print('Getting Deployed Images ...')
    images = pc_api.images_list_read(args.image_id)
    optional_print(str(len(images))+' images total')
    for image in images:
        image_id = image['_id']
        vulns = image['vulnerabilities']
        if not vulns:
 #       optional_print('No vulns for '+image_id)
            continue
        keep = False
        for vuln in vulns:
            if vuln['cve'] == args.cve:
                keep = True
                optional_print('Image '+image_id+' is vulnerable to '+args.cve)
                break
        if not keep:
#        optional_print('Excluding '+image_id)
            continue
        optional_print('Locations for '+image['_id'])
        containers = pc_api.containers_list_read(image['id'])
        for container in containers:
            if 'cluster' in container['info']:
                optional_print(container['info']['imageName']+': '+container['info']['cluster'])
            else:
                optional_print(container['info']['imageName']+': no cluster info. Falling back to hostname: '+ container['hostname'])
        optional_print()
