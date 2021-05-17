from __future__ import print_function
from pc_lib import pc_api, pc_utility

import json

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--mode',
    type=str,
    choices=['ci', 'deployed', 'all'],
    default='all',
    help='(Optional) - Report on CI, Deployed, or all Images.')
parser.add_argument(
    '--package_type',
    type=str,
    choices=['binary', 'gem', 'go', 'jar', 'nodejs', 'nuget', 'package', 'python', 'windows', 'all'],
    default='all',
    help='(Optional) - Report on one or all Package Types.')
parser.add_argument(
    '--image_id',
    type=str,
    help='(Optional) - ID of the Image (sha256:...).')
parser.add_argument(
    '--package_id',
    type=str,
    help='(Optional) - ID of the Package (name:version).')
args = parser.parse_args()

search_package_name    = None
search_package_version = None

if args.package_id:
   output_mode = 'quiet'
   if ':' in args.package_id:
       [search_package_name, search_package_version] = args.package_id.split(':')
   else:
       search_package_name = args.package_id
else:
   output_mode = 'verbose'

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)
pc_api.validate_api_compute()

# --Main-- #

get_deployed_images = True
get_ci_images       = True

deployed_images_with_package = []
ci_images_with_package       = []

"""
"instances": [{
	"image": "k8s.gcr.io/etcd:3.4.3-0",
    "host": "demo",
    "registry": "k8s.gcr.io"
    "repo": "etcd",
    "tag": "3.4.3-0",
	}],
"packages": [{
    "pkgsType": "package",
    "pkgs": [{
		"version": "2.27-2",
		"name": "grep",
		"cveCount": 12,
		"license": "GPL-3+",
		"layerTime": 1557275612
	}],
"""

"""
"pkgsType": [
    "binary",
    "gem",
    "go",
    "jar",
    "nodejs",
    "nuget",
    "package",
    "python",
    "windows",
]
"""

print('Testing Compute API Access ...', end='')
intelligence = pc_api.statuses_intelligence()
print(' done.')
print()

if search_package_name:
    print('Searching for Package: (%s) Version: (%s)' % (search_package_name, search_package_version))
    print()

# Monitor > Vulnerabilities/Compliance > Images > Deployed
if args.mode in ['deployed', 'all']:
    print('Getting Deployed Images ...')
    deployed_images = {}
    images = pc_api.images_list_read(args.image_id)
    for image in images:
        image_id = image['id']
        # TODO: Verify instances array length.
        image_ii = '%s %s' % (image['instances'][0]['image'], image['instances'][0]['host'])
        deployed_images[image_id] = {
            'id':        image['id'],
            'instance':  image_ii,
            'instances': image['instances'],
            'packages':  image['packages']}
    pc_api.progress(mode=output_mode)
    for image in deployed_images:
        pc_api.progress('Deployed Image', mode=output_mode)
        pc_api.progress('ID: %s' % image, mode=output_mode)
        pc_api.progress('Instance: %s' % deployed_images[image]['instance'], mode=output_mode)
        pc_api.progress(mode=output_mode)
        for package_type in deployed_images[image]['packages']:
            for package in package_type['pkgs']:
                pc_api.progress('\tType: %s' % package_type['pkgsType'], mode=output_mode)
                pc_api.progress('\tName: %s' % package['name'], mode=output_mode)
                pc_api.progress('\tVers: %s' % package['version'], mode=output_mode)
                pc_api.progress('\tCVEs: %s' % package['cveCount'], mode=output_mode)
                pc_api.progress(mode=output_mode)
                if args.package_type in [package_type['pkgsType'], 'all']:
                    if search_package_name and (search_package_name == package['name']):
                           if search_package_version:
                               if search_package_version == package['version']:
                                   deployed_images_with_package.append(deployed_images[image]['instance'])
                           else:
                               deployed_images_with_package.append(deployed_images[image]['instance'])
    print('Done.')
    print()

# Monitor > Vulnerabilities/Compliance > Images > CI
if args.mode in ['ci', 'all']:
    print('Getting CI Images ...')
    ci_images = {}
    images = pc_api.scans_list_read(args.image_id)
    for image in images:
        image_id = image['entityInfo']['id']
        if image['entityInfo']['instances']:
            image_ii = '%s %s' % (image['entityInfo']['instances'][0]['image'], image['entityInfo']['instances'][0]['host'])
        else:
            image_ii = None
        ci_images[image_id] = {
            'id':        image['entityInfo']['id'],
            'instance':  image_ii,
            'instances': image['entityInfo']['instances'],
            'packages':  image['entityInfo']['packages']}
    pc_api.progress(mode=output_mode)
    for image in ci_images:
        pc_api.progress('CI Image', mode=output_mode)
        pc_api.progress('ID: %s' % image, mode=output_mode)
        pc_api.progress('Instance: %s' % ci_images[image]['instance'], mode=output_mode)
        pc_api.progress(mode=output_mode)
        for package_type in ci_images[image]['packages']:
            for package in package_type['pkgs']:
                pc_api.progress('\tType: %s' % package_type['pkgsType'], mode=output_mode)
                pc_api.progress('\tName: %s' % package['name'], mode=output_mode)
                pc_api.progress('\tVers: %s' % package['version'], mode=output_mode)
                pc_api.progress('\tCVEs: %s' % package['cveCount'], mode=output_mode)
                pc_api.progress(mode=output_mode)
                if args.package_type in [package_type['pkgsType'], 'all']:
                    if search_package_name and (search_package_name == package['name']):
                           if search_package_version:
                               if search_package_version == package['version']:
                                   ci_images_with_package.append(deployed_images[image]['instance'])
                           else:
                               ci_images_with_package.append(deployed_images[image]['instance'])
    print('Done.')
    print()

if args.package_id:
    if args.mode in ['deployed', 'all']:
        print()
        if deployed_images_with_package:
            print('Package: (%s) Version: (%s) found in these Deployed Images:' % (search_package_name, search_package_version))
            print()
            for image in deployed_images_with_package:
                print('\t%s' % image)
        else:
            print('Package: (%s) Version: (%s) not found in any Deployed Images' % (search_package_name, search_package_version))
    if args.mode in ['ci', 'all']:
        print()
        if ci_images_with_package:
            print('Package: (%s) Version: (%s) found in these CI Images:' % (search_package_name, search_package_version))
            print()
            for image in ci_images_with_package:
                print('\t%s' % image)
        else:
            print('Package: (%s) Version: (%s) not found in any CI Images' % (search_package_name, search_package_version))
    