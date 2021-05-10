from __future__ import print_function
from pc_lib import pc_api, pc_utility

import json

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--image_id',
    type=str,
    help='ID of the Image (sha256:...).')
parser.add_argument(
    '--package_id',
    type=str,
    help='ID of the Package (name:version).')
args = parser.parse_args()

search_package_name    = None
search_package_version = None

if args.package_id:
   if ':' in args.package_id:
       [search_package_name, search_package_version] = args.package_id.split(':')
   else:
       search_package_name = args.package_id

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)
pc_api.validate_api_compute()

# --Main-- #

pc_api.login()

get_deployed_images = True
get_ci_images = True
qlimit = 50

deployed_images_with_package = []
ci_images_with_package = []

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
		}, {
"""

if search_package_name:
    print('Searching for Package: (%s) Version: (%s)' % (search_package_name, search_package_version))
    print()

# Monitor > Vulnerabilities > Images > Deployed
print('Getting Deployed Images ...')
deployed_images = {}
offset = 0
while get_deployed_images:
    if args.image_id:
        images = pc_api.execute_compute('GET', 'api/v1/images?id=%s&filterBaseImage=true&limit=%s&offset=%s' % (args.image_id, qlimit, offset))
    else:
        images = pc_api.execute_compute('GET', 'api/v1/images?filterBaseImage=true&limit=%s&offset=%s' % (qlimit, offset))
    if not images:
        get_deployed_images = False
        break
    for image in images:
        image_id = image['id']
        # TODO: Verify instances array length.
        image_ii = '%s %s' % (image['instances'][0]['image'], image['instances'][0]['host'])
        # print(image_id)
        deployed_images[image_id] = {
            'id':        image['id'],
            'instance':  image_ii,
            'instances': image['instances'],
            'packages':  image['packages']}
    offset = offset + qlimit
print()

for image in deployed_images:
    print('Deployed Image  ')
    print('ID: %s' % image)
    print('Instance: %s' % deployed_images[image]['instance'])
    print()
    for package_type in deployed_images[image]['packages']:
        for package in package_type['pkgs']:
            print('\tType: %s' % package_type['pkgsType'])
            print('\tName: %s' % package['name'])
            print('\tVers: %s' % package['version'])
            print('\tCVEs: %s' % package['cveCount'])
            print()
            if package_type['pkgsType'] == 'package':
                if search_package_name and (search_package_name == package['name']):
                       if search_package_version:
                           if search_package_version == package['version']:
                               deployed_images_with_package.append(deployed_images[image]['instance'])
                       else:
                           deployed_images_with_package.append(deployed_images[image]['instance'])
    print()

# Monitor > Vulnerabilities > Images > CI
print('Getting CI Images ...')
ci_images = {}
offset = 0
while get_ci_images:
    if args.image_id:
        images = pc_api.execute_compute('GET', 'api/v1/scans?imageID=%s&filterBaseImage=true&limit=%s&offset=%s' % (args.image_id, qlimit, offset))
    else:
        images = pc_api.execute_compute('GET', 'api/v1/scans?filterBaseImage=true&limit=%s&offset=%s' % (qlimit, offset))
    if not images:
        get_ci_images = False
        break
    for image in images:
        image_id = image['entityInfo']['id']
        if image['entityInfo']['instances']:
            image_ii = '%s %s' % (image['entityInfo']['instances'][0]['image'], image['entityInfo']['instances'][0]['host'])
        else:
            image_ii = None
        # print(image_id)
        ci_images[image_id] = {
            'id':        image['entityInfo']['id'],
            'instance':  image_ii,
            'instances': image['entityInfo']['instances'],
            'packages':  image['entityInfo']['packages']}
    offset = offset + qlimit
print()

for image in ci_images:
    print('CI Image')
    print('ID: %s' % image)
    print('Instance: %s' % ci_images[image]['instance'])
    print()
    for package_type in ci_images[image]['packages']:
        for package in package_type['pkgs']:
            print('\tType: %s' % package_type['pkgsType'])
            print('\tName: %s' % package['name'])
            print('\tVers: %s' % package['version'])
            print('\tCVEs: %s' % package['cveCount'])
            print()
            if package_type['pkgsType'] == 'package':
                if search_package_name and (search_package_name == package['name']):
                       if search_package_version:
                           if search_package_version == package['version']:
                               ci_images_with_package.append(deployed_images[image]['instance'])
                       else:
                           ci_images_with_package.append(deployed_images[image]['instance'])
    print()

if args.package_id:
    print()
    if deployed_images_with_package:
        print('Package: (%s) Version: (%s) found in these Deployed images:' % (search_package_name, search_package_version))
        print()
        for image in deployed_images_with_package:
            print('\t%s' % image)
    else:
        print('Package: (%s) Version: (%s) not found in any Deployed images' % (search_package_name, search_package_version))

    print()
    if ci_images_with_package:
        print('Package: (%s) Version: (%s) found in these CI images:' % (search_package_name, search_package_version))
        print()
        for image in ci_images_with_package:
            print('\t%s' % image)
    else:
        print('Package: (%s) Version: (%s) not found in any CI images' % (search_package_name, search_package_version))
    