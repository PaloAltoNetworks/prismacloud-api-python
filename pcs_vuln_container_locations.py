""" Get a list of vulnerable containers and their clusters """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--cve',
    type=str,
    required=True,
    help='(Required) - ID of the CVE.')
parser.add_argument(
    '--image_id',
    type=str,
    help='(Optional) - ID of the Image (sha256:...).')
parser.add_argument(
    '--mode',
    type=str,
    choices=['registry', 'deployed', 'all'],
    default='all',
    help='(Optional) - Report on Registry, Deployed, or all Images.')
args = parser.parse_args()

# --Helpers-- #

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)
pc_api.validate_api_compute()

# --Main-- #

print('Testing Compute API Access ...', end='')
intelligence = pc_api.statuses_intelligence()
print(' done.')
print()

print('Searching for CVE: (%s) Limiting Search to Image ID: (%s)' % (args.cve, args.image_id))
print()

# Monitor > Vulnerabilities/Compliance > Images > Registries
if args.mode in ['registry', 'all']:
    registry_images = pc_api.registry_list_read(args.image_id)
    print('Getting Registry Images ...', end='')
    print(' done.')
    print('Found %s Registry Images' % len(registry_images))
    print()
    for image in registry_images:
        image_id = image['_id']
        vulnerabilities = image['vulnerabilities']
        if not vulnerabilities:
            # print('No vulnerabilities for Image ID: %s' % image_id)
            continue
        vulnerable = False
        for vulnerability in vulnerabilities:
            if args.cve and vulnerability['cve'] == args.cve:
                vulnerable = True
                # print('Image ID: %s is vulnerable to CVE: %s' % (image_id, args.cve))
                break
        if not vulnerable:
            # print('Excluding Image ID: %s is not vulnerable to CVE: %s' % (image_id, args.cve))
            continue
        print('Locations for vulnerable Registry Image ID: %s ' % image_id)
        print('\tRegistry: %s' % image['repoTag']['registry'])
        print('\tRepo: %s' % image['repoTag']['repo'])
        print('\tTag: %s' % image['repoTag']['tag'])
        print()
    print()

# Monitor > Vulnerabilities/Compliance > Images > Deployed
if args.mode in ['deployed', 'all']:
    print('Getting Deployed Images ...', end='')
    deployed_images = pc_api.images_list_read(image_id=args.image_id, query_params={'filterBaseImage': 'true'})
    print(' done.')
    print('Found %s Deployed Images' % len(deployed_images))
    print()
    for image in deployed_images:
        image_id = image['_id']
        vulnerabilities = image['vulnerabilities']
        if not vulnerabilities:
            # print('No vulnerabilities for Image ID: %s' % image_id)
            continue
        vulnerable = False
        for vulnerability in vulnerabilities:
            if args.cve and vulnerability['cve'] == args.cve:
                vulnerable = True
                # print('Image ID: %s is vulnerable to CVE: %s' % (image_id, args.cve))
                break
        if not vulnerable:
            # print('Excluding Image ID: %s is not vulnerable to CVE: %s' % (image_id, args.cve))
            continue
        print('Locations for vulnerable Deployed Image ID: %s ' % image_id)
        containers = pc_api.containers_list_read(image_id=image_id)
        if not containers:
            print('\tNo containers found for this image')
            continue
        for container in containers:
            print('\tImage Name: %s' % container['info']['imageName'])
            if 'cluster' in container['info']:
                print('\tCluster:    %s' % container['info']['cluster'])
            else:
                print('\tHostname:   %s' % container['hostname'])
        print()
