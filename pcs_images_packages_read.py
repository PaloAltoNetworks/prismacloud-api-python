""" Get a list of Packages in CI, Registry, Deployed, or all Images """

from __future__ import print_function
from packaging import version
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
    help='(Optional) - ID of the Package (format: name:version) with :version being optional. Example: zipp:3.6.0')
parser.add_argument(
    '--exact_match_name',
    type=bool,
    choices=[True, False],
    default=False,
    help='(Optional) - True, Package name must exactly match (Default). False, use substring matching of Package name.')
parser.add_argument(
    '--version_comparison',
    type=str,
    choices=['eq', 'gt', 'lt'],
    default='eq',
    help="(Optional) - Package version must be equal (Default), greater than, or less than the version specified in the 'package_id' parameter.")
parser.add_argument(
    '--output_to_csv',
    type=bool,
    choices=[True, False],
    default=False,
    help="(Optional) - Output results to CSV files ('ci.csv', 'registry.csv', 'deployed.csv')."
)

args = parser.parse_args()
search_package_name    = None
search_package_version = None
print_all_packages = True
if args.package_id:
    print_all_packages = False
    if ':' in args.package_id:
        [search_package_name, search_package_version] = args.package_id.split(':')
    else:
        search_package_name = args.package_id

# --Helpers-- #

def optional_print(txt='', mode=True):
    if mode:
        print(txt)

def package_name_matches(exact_match_name, search_name, package_name):
    if not search_name or not package_name:
        return False
    if (exact_match_name and search_name == package_name) or (search_name in package_name):
        return True
    return False

def package_version_matches(version_comparison, search_version, package_version):
    if not search_version or not package_version:
        return False
    search_semver = version.parse(search_version)
    package_semver = version.parse(package_version)
    # In the future, use match/case provided by Python 3.10.
    if version_comparison == 'eq' and search_semver == package_semver:
        return True
    if version_comparison == 'gt' and search_semver < package_semver:
        return True
    if version_comparison == 'lt' and search_semver > package_semver:
        return True
    return False

def write_file(file_name, header, data):
    with open(file_name, 'w') as data_file:
        data_file.write('%s\n' % header)
        data_file.write("\n".join(data))

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

csv_header = 'Instance\tPackage Type\tPackage Name\tPackage Version\tPackage Path'

# Example response from the API.

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
    print('Searching for Package: (%s) Version: (%s) Exact Match Name: (%s) Version Comparison Operator: (%s)' % (search_package_name, search_package_version, args.exact_match_name, args.version_comparison))
    print()

# Monitor > Vulnerabilities/Compliance > Images > CI
ci_images = {}
if args.mode in ['ci', 'all']:
    print('Getting CI Images ...')
    images = pc_api.scans_list_read(args.image_id)
    for image in images:
        image_id = image['entityInfo']['id']
        if image['entityInfo']['instances']:
            try:
                image_ii = '%s %s' % (image['entityInfo']['instances'][0]['image'], image['entityInfo']['instances'][0]['host'])
            except KeyError:
                image_ii = ''
        else:
            image_ii = ''
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
                    if package_name_matches(args.exact_match_name, search_package_name, package['name']):
                        if search_package_version:
                            if package_version_matches(args.version_comparison, search_package_version, package['version']):
                                ci_images_with_package.append("%s\t%s\t%s\t%s\t%s" % (ci_images[image]['instance'], packages['pkgsType'], package['name'], package['version'], package_path))
                        else:
                            ci_images_with_package.append("%s\t%s\t%s\t%s\t%s" % (ci_images[image]['instance'], packages['pkgsType'], package['name'], package['version'], package_path))
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
        except KeyError:
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
                    if package_name_matches(args.exact_match_name, search_package_name, package['name']):
                        if search_package_version:
                            if package_version_matches(args.version_comparison, search_package_version, package['version']):
                                registry_images_with_package.append("%s\t%s\t%s\t%s\t%s" % (registry_images[image]['instance'], packages['pkgsType'], package['name'], package['version'], package_path))
                        else:
                            registry_images_with_package.append("%s\t%s\t%s\t%s\t%s" % (registry_images[image]['instance'], packages['pkgsType'], package['name'], package['version'], package_path))
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
        except KeyError:
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
                    if package_name_matches(args.exact_match_name, search_package_name, package['name']):
                        if search_package_version:
                            if package_version_matches(args.version_comparison, search_package_version, package['version']):
                                deployed_images_with_package.append("%s\t%s\t%s\t%s\t%s" % (deployed_images[image]['instance'], packages['pkgsType'], package['name'], package['version'], package_path))
                        else:
                            deployed_images_with_package.append("%s\t%s\t%s\t%s\t%s" % (deployed_images[image]['instance'], packages['pkgsType'], package['name'], package['version'], package_path))
    print('Done.')
    print()

if args.package_id:
    if args.mode in ['ci', 'all']:
        print()
        if ci_images_with_package:
            print('Package found in these CI Images:')
            print()
            for image in ci_images_with_package:
                print('\t%s' % image)
            if args.output_to_csv:
                write_file('ci.csv', csv_header, ci_images_with_package)
                print()
                print('Output to ci.csv')
        else:
            print('Package not found in any CI Images')
    if args.mode in ['registry', 'all']:
        print()
        if registry_images_with_package:
            print('Package found in these Registry Images:')
            print()
            for image in registry_images_with_package:
                print('\t%s' % image)
            if args.output_to_csv:
                write_file('registry.csv', csv_header, registry_images_with_package)
                print()
                print('Output to registry.csv')
        else:
            print('Package not found in any Registry Images')
    if args.mode in ['deployed', 'all']:
        print()
        if deployed_images_with_package:
            print('Package found in these Deployed Images:')
            print()
            for image in deployed_images_with_package:
                print('\t%s' % image)
            if args.output_to_csv:
                write_file('deployed.csv', csv_header, deployed_images_with_package)
                print()
                print('Output to deployed.csv')
        else:
            print('Package not found in any Deployed Images')
