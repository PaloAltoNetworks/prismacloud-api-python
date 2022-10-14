""" Get a list of Packages in CI, Registry, Deployed, or all Images """

from packaging import version

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--image_id',
    type=str,
    help='(Optional) - ID of the Image (sha256:...).')
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
    '--version_comparison', # version_comparison_operator
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
if args.package_id:
    if ':' in args.package_id:
        [search_package_name, search_package_version] = args.package_id.split(':')
    else:
        search_package_name = args.package_id
    search_all_packages = False
else:
    search_all_packages = True

# --Helpers-- #

def optional_print(txt='', mode=True):
    if mode:
        print(txt)

def package_name_matches(comparison_exact, search_name, package_name):
    if not search_name or not package_name:
        return False
    if (comparison_exact and search_name == package_name) or (search_name in package_name):
        return True
    return False

def package_version_matches(comparison_operator, search_version, package_version):
    if not search_version or not package_version:
        return False
    search_semver = version.parse(search_version)
    package_semver = version.parse(package_version)
    # In the future, use match/case provided by Python 3.10.
    if comparison_operator == 'eq' and search_semver == package_semver:
        return True
    if comparison_operator == 'gt' and search_semver < package_semver:
        return True
    if comparison_operator == 'lt' and search_semver > package_semver:
        return True
    return False

# Write a header and an array of data to a CSV file.

def write_file(file_name, header, data):
    with open(file_name, 'w') as data_file:
        data_file.write('%s\n' % header)
        data_file.write('\n'.join(data))

# Parse response from the API.

# pylint: disable=too-many-branches
def parse_images(images, output_mode, search_package_type, search_exact_name, search_name, search_comparison_operator, search_version):
    normalized_images = {}
    images_with_package = []
    for image in images:
        image_id = image['_id']
        if 'entityInfo' in image:
            try:
                image_ii = '%s %s' % (image['entityInfo']['instances'][0]['image'], image['entityInfo']['instances'][0]['host'])
            except IndexError:
                image_ii = ''
            except KeyError:
                image_ii = ''
            except TypeError:
                image_ii = ''
            normalized_images[image_id] = {
                'id':        image_id,
                'instance':  image_ii,
                'instances': image['entityInfo']['instances'],
                'packages':  image['entityInfo']['packages']}
        else:
            try:
                image_ii = '%s %s' % (image['instances'][0]['image'], image['instances'][0]['host'])
            except IndexError:
                image_ii = ''
            except KeyError:
                image_ii = ''
            except TypeError:
                image_ii = ''
            normalized_images[image_id] = {
                'id':        image_id,
                'instance':  image_ii,
                'instances': image['instances'],
                'packages':  image['packages']}
    optional_print(mode=search_all_packages)
    for image in normalized_images:
        optional_print('Image', mode=output_mode)
        optional_print('ID: %s' % image, mode=output_mode)
        optional_print('Instance: %s' % normalized_images[image]['instance'], mode=output_mode)
        optional_print(mode=output_mode)
        if not normalized_images[image]['packages']:
            continue
        for packages in normalized_images[image]['packages']:
            for package in packages['pkgs']:
                optional_print('\tType: %s' % packages['pkgsType'], mode=output_mode)
                optional_print('\tName: %s' % package['name'], mode=output_mode)
                optional_print('\tVers: %s' % package['version'], mode=output_mode)
                if 'path' in package:
                    optional_print('\tPath: %s' % package['path'], mode=output_mode)
                    package_path = package['path']
                else:
                    package_path = ''
                optional_print('\tCVEs: %s' % package['cveCount'], mode=output_mode)
                optional_print(mode=output_mode)
                if search_package_type in [packages['pkgsType'], 'all']:
                    if package_name_matches(search_exact_name, search_name, package['name']):
                        if search_version:
                            if package_version_matches(search_comparison_operator, search_version, package['version']):
                                images_with_package.append("%s\t%s\t%s\t%s\t%s" % (normalized_images[image]['instance'], packages['pkgsType'], package['name'], package['version'], package_path))
                        else:
                            images_with_package.append("%s\t%s\t%s\t%s\t%s" % (normalized_images[image]['instance'], packages['pkgsType'], package['name'], package['version'], package_path))
    return images_with_package

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

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)
pc_api.validate_api_compute()

# --Main-- #

print('Testing Compute API Access ...', end='')
intelligence = pc_api.statuses_intelligence()
print(' done.')
print()

ci_images_with_package       = []
registry_images_with_package = []
deployed_images_with_package = []

csv_header = 'Instance\tPackage Type\tPackage Name\tPackage Version\tPackage Path'

if search_package_name:
    print('Searching for Package: (%s) Version: (%s) Exact Match Name: (%s) Version Comparison Operator: (%s)' % (search_package_name, search_package_version, args.exact_match_name, args.version_comparison))
    print()

# Monitor > Vulnerabilities/Compliance > Images > CI
if args.mode in ['ci', 'all']:
    print('Getting CI Images ...')
    ci_images = pc_api.scans_list_read(args.image_id)
    ci_images_with_package = parse_images(ci_images, search_all_packages, args.package_type, args.exact_match_name, search_package_name, args.version_comparison, search_package_version)
    print('Done.')
    print()

# Monitor > Vulnerabilities/Compliance > Images > Registries
if args.mode in ['registry', 'all']:
    print('Getting Registry Images ...')
    registry_images = pc_api.registry_list_read(args.image_id)
    registry_images_with_package = parse_images(registry_images, search_all_packages, args.package_type, args.exact_match_name, search_package_name, args.version_comparison, search_package_version)
    print('Done.')
    print()

# Monitor > Vulnerabilities/Compliance > Images > Deployed
if args.mode in ['deployed', 'all']:
    print('Getting Deployed Images ...')
    deployed_images = pc_api.images_list_read(image_id=args.image_id, query_params={'filterBaseImage': 'true'})
    deployed_images_with_package = parse_images(deployed_images, search_all_packages, args.package_type, args.exact_match_name, search_package_name, args.version_comparison, search_package_version)
    print('Done.')
    print()

# Output images with the specified package, when a package is specified.
if search_package_name:
    if args.mode in ['ci', 'all']:
        print()
        if ci_images_with_package:
            print('Package found in these CI Images:')
            print()
            for ci_image in ci_images_with_package:
                print('\t%s' % ci_image)
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
            for registry_image in registry_images_with_package:
                print('\t%s' % registry_image)
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
            for deployed_image in deployed_images_with_package:
                print('\t%s' % deployed_image)
            if args.output_to_csv:
                write_file('deployed.csv', csv_header, deployed_images_with_package)
                print()
                print('Output to deployed.csv')
        else:
            print('Package not found in any Deployed Images')
