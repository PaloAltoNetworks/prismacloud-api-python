from pc_lib import pc_api, pc_utility

import json

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--image_id',
    type=str,
    help='ID of the Image (sha256:...).')
parser.add_argument(
    '--compute_endpoint',
    type=str,
    required=True,
    help='Compute Endpoint (See Compute > Manage > System > Downloads: Path to Console).')
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

pc_api.login()

redlock_api = pc_api.api
twistlock_api = args.compute_endpoint.replace('http://', '')
pc_api.api = twistlock_api

get_deployed_images = True
get_ci_images = True
qlimit = 50

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

# Monitor > Vulnerabilities > Images > Deployed
print('Getting Deployed Images ...')
deployed_images = {}
offset = 0
while get_deployed_images:
    if args.image_id:
        images = pc_api.execute('GET', 'api/v1/images?id=%s&filterBaseImage=true&limit=%s&offset=%s' % (args.image_id, qlimit, offset))
    else:
        images = pc_api.execute('GET', 'api/v1/images?filterBaseImage=true&limit=%s&offset=%s' % (qlimit, offset))
    if not images:
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
    print()

# Monitor > Vulnerabilities > Images > CI
print('Getting CI Images ...')
ci_images = {}
offset = 0
while get_ci_images:
    if args.image_id:
        images = pc_api.execute('GET', 'api/v1/scans?imageID=%s&filterBaseImage=true&limit=%s&offset=%s' % (args.image_id, qlimit, offset))
    else:
        images = pc_api.execute('GET', 'api/v1/scans?filterBaseImage=true&limit=%s&offset=%s' % (qlimit, offset))
    if not images:
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
    print()

