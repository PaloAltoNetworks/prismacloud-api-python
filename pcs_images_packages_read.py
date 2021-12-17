""" Get a list of Packages in CI, Deployed, or all Images """

from __future__ import print_function
from pc_lib import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--mode',
    type=str,
    choices=['ci', 'registry', 'deployed', 'all'],
    default='all',
    help='(Optional) - Report on CI, Registry, Deployed, or all Images.')
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
    help='(Optional) - ID of the Package (name:version) with version being optional.')
parser.add_argument(
    '--search_package_substring',
    type=bool,
    choices=[True,False],
    default=False,
    help='(Optional) - True, package id will match if value is contained package name. False, package id must be exact. default'

)

args = parser.parse_args()

search_package_name    = None
search_package_version = None

if args.package_id:
    print_all_packages = False
    if ':' in args.package_id:
        [search_package_name, search_package_version] = args.package_id.split(':')
    else:
        search_package_name = args.package_id
else:
    print_all_packages = True

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

# Monitor > Vulnerabilities/Compliance > Images > CI
ci_images = {}
if args.mode in ['ci', 'all']:
    print('Getting CI Images ...')
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
    optional_print(mode=print_all_packages)
    for image in ci_images:
        optional_print('CI Image', mode=print_all_packages)
        optional_print('ID: %s' % image, mode=print_all_packages)
        optional_print('Instance: %s' % ci_images[image]['instance'], mode=print_all_packages)
        optional_print(mode=print_all_packages)
        if not ci_images[image]['packages']:
            continue
        for packages in ci_images[image]['packages']:
            for package in packages['pkgs']:
                optional_print('\tType: %s' % packages['pkgsType'], mode=print_all_packages)
                optional_print('\tName: %s' % package['name'], mode=print_all_packages)
                optional_print('\tVers: %s' % package['version'], mode=print_all_packages)
                if 'path' in package:
                    optional_print('\tPath: %s' % package['path'], mode=print_all_packages)
                    package_path = package['path']
                else:
                    package_path = ''
                optional_print('\tCVEs: %s' % package['cveCount'], mode=print_all_packages)
                optional_print(mode=print_all_packages)
                if args.package_type in [packages['pkgsType'], 'all']:
                    if search_package_name and (search_package_name == package['name'] or (args.search_package_substring and search_package_name in package['name'])):
                        if search_package_version:
                            if search_package_version == package['version']:
                                ci_images_with_package.append("%s: %s %s %s %s" % (ci_images[image]['instance'], packages['pkgsType'], package['name'], package['version'], package_path))
                        else:
                            ci_images_with_package.append("%s: %s %s %s %s" % (ci_images[image]['instance'], packages['pkgsType'], package['name'], package['version'], package_path))
    print('Done.')
    print()

# Monitor > Vulnerabilities/Compliance > Images > Registries
registry_images = {}
if args.mode in ['registry', 'all']:
    print('Getting Registry Images ...')
    images = pc_api.registry_list_read(args.image_id)
    for image in images:
        image_id = image['_id']
        try:
            image_ii = '%s %s' % (image['instances'][0]['image'], image['instances'][0]['host'])
        except Exception:
            image_ii = ''
        registry_images[image_id] = {
            'id':        image['_id'],
            'instance':  image_ii,
            'instances': image['instances'],
            'packages':  image['packages']}
    optional_print(mode=print_all_packages)
    for image in registry_images:
        optional_print('Registry Image', mode=print_all_packages)
        optional_print('ID: %s' % image, mode=print_all_packages)
        optional_print('Instance: %s' % registry_images[image]['instance'], mode=print_all_packages)
        optional_print(mode=print_all_packages)
        if not registry_images[image]['packages']:
            continue
        for packages in registry_images[image]['packages']:
            for package in packages['pkgs']:
                optional_print('\tType: %s' % packages['pkgsType'], mode=print_all_packages)
                optional_print('\tName: %s' % package['name'], mode=print_all_packages)
                optional_print('\tVers: %s' % package['version'], mode=print_all_packages)
                if 'path' in package:
                    optional_print('\tPath: %s' % package['path'], mode=print_all_packages)
                    package_path = package['path']
                else:
                    package_path = ''
                optional_print('\tCVEs: %s' % package['cveCount'], mode=print_all_packages)
                optional_print(mode=print_all_packages)
                if args.package_type in [packages['pkgsType'], 'all']:
                    if search_package_name and (search_package_name == package['name'] or (args.search_package_substring and search_package_name in package['name'])):
                        if search_package_version:
                            if search_package_version == package['version']:
                                registry_images_with_package.append("%s: %s %s %s %s" % (registry_images[image]['instance'], packages['pkgsType'], package['name'], package['version'], package_path))
                        else:
                            registry_images_with_package.append("%s: %s %s %s %s" % (registry_images[image]['instance'], packages['pkgsType'], package['name'], package['version'], package_path))
    print('Done.')
    print()

# Monitor > Vulnerabilities/Compliance > Images > Deployed
deployed_images = {}
if args.mode in ['deployed', 'all']:
    print('Getting Deployed Images ...')
    images = pc_api.images_list_read(args.image_id)
    for image in images:
        image_id = image['_id']
        try:
            image_ii = '%s %s' % (image['instances'][0]['image'], image['instances'][0]['host'])
        except Exception:
            image_ii = ''
        deployed_images[image_id] = {
            'id':        image['_id'],
            'instance':  image_ii,
            'instances': image['instances'],
            'packages':  image['packages']}
    optional_print(mode=print_all_packages)
    for image in deployed_images:
        optional_print('Deployed Image', mode=print_all_packages)
        optional_print('ID: %s' % image, mode=print_all_packages)
        optional_print('Instance: %s' % deployed_images[image]['instance'], mode=print_all_packages)
        optional_print(mode=print_all_packages)
        if not deployed_images[image]['packages']:
            continue
        for packages in deployed_images[image]['packages']:
            for package in packages['pkgs']:
                optional_print('\tType: %s' % packages['pkgsType'], mode=print_all_packages)
                optional_print('\tName: %s' % package['name'], mode=print_all_packages)
                optional_print('\tVers: %s' % package['version'], mode=print_all_packages)
                if 'path' in package:
                    optional_print('\tPath: %s' % package['path'], mode=print_all_packages)
                    package_path = package['path']
                else:
                    package_path = ''
                optional_print('\tCVEs: %s' % package['cveCount'], mode=print_all_packages)
                optional_print(mode=print_all_packages)
                if args.package_type in [packages['pkgsType'], 'all']:
                    if search_package_name and (search_package_name == package['name'] or (args.search_package_substring and search_package_name in package['name'])):
                        if search_package_version:
                            if search_package_version == package['version']:
                                deployed_images_with_package.append("%s: %s %s %s %s" % (deployed_images[image]['instance'], packages['pkgsType'], package['name'], package['version'], package_path))
                        else:
                            deployed_images_with_package.append("%s: %s %s %s %s" % (deployed_images[image]['instance'], packages['pkgsType'], package['name'], package['version'], package_path))
    print('Done.')
    print()

if args.package_id:
    if args.mode in ['ci', 'all']:
        print()
        if ci_images_with_package:
            print('Package: (%s) Version: (%s) found in these CI Images:' % (search_package_name, search_package_version))
            print()
            for image in ci_images_with_package:
                print('\t%s' % image)
        else:
            print('Package: (%s) Version: (%s) not found in any CI Images' % (search_package_name, search_package_version))
    if args.mode in ['registry', 'all']:
        print()
        if registry_images_with_package:
            print('Package: (%s) Version: (%s) found in these Registry Images:' % (search_package_name, search_package_version))
            print()
            for image in registry_images_with_package:
                print('\t%s' % image)
        else:
            print('Package: (%s) Version: (%s) not found in any Registry Images' % (search_package_name, search_package_version))
    if args.mode in ['deployed', 'all']:
        print()
        if deployed_images_with_package:
            print('Package: (%s) Version: (%s) found in these Deployed Images:' % (search_package_name, search_package_version))
            print()
            for image in deployed_images_with_package:
                print('\t%s' % image)
        else:
            print('Package: (%s) Version: (%s) not found in any Deployed Images' % (search_package_name, search_package_version))
