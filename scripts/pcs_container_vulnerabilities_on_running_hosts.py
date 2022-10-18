""" Get Vulnerabilities in Containers (Deployed Images) """

import json
import csv

from datetime import datetime

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

DEFAULT_FILE_NAME = 'vulnerabilities.csv'

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--csv_file_name',
    type=str,
    default=DEFAULT_FILE_NAME,
    help="(Optional) - Export to the given file name. (Default %s)" % DEFAULT_FILE_NAME
)
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)
pc_api.validate_api_compute()

# --Helpers-- #

def datetime_or_empty(datetime_string):
    if int(datetime_string) == 0:
        return ""
    return datetime.utcfromtimestamp(int(datetime_string)).strftime('%Y-%m-%d %H:%M:%S')

# --Main-- #

print('Testing Compute API Access ...', end='')
intelligence = pc_api.statuses_intelligence()
print(' done.')
print()

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
containers_list = pc_api.containers_list_read()
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
        #print(json.dumps(image, indent=4))
    image_id = image['_id']
    images_dictionary[image_id] = image

print("* Exporting Vulnerabilities (please wait) ...")

# pylint: disable=line-too-long
headers = ['Registry','Repository','Tag','Id','Distro','Hosts','Layer','CVE ID','Compliance ID','Type','Severity','Packages','Source Package','Package Version','Package License','CVSS','Fix Status','Fix Date','Grace Days','Risk Factors','Vulnerability Tags','Description','Cause','Containers','Custom Labels','Published','Discovered','Binaries','Clusters','Namespaces','Collections','Digest','Vulnerability Link','Apps','Package Path']

with open(args.csv_file_name, 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for container in containers_list:
        if pc_api.debug:
            print("#########################################################################")
            print(json.dumps(container, indent=4))
        if 'imageID' in container['info']:
            image_id   = container['info']['imageID']
            image_name = container['info']['imageName']
            host_name = container['hostname']
            # If the host is in our hosts dictionary, then the host is running.
            if host_name in hosts_dictionary:
                host = hosts_dictionary[host_name]
                if image_id in images_dictionary:
                    image = images_dictionary[image_id]
                    packages_dictionary = {}
                    if 'packages' in image:
                        for package in image['packages']:
                            if 'pkgs' in package:
                                for pkg in package['pkgs']:
                                    if 'name' in pkg and 'version' in pkg:
                                        packages_dictionary[pkg['name'] + pkg['version']] = pkg
                    if 'vulnerabilities' in images_dictionary[image_id] and images_dictionary[image_id]['vulnerabilities']:
                        vulnerabilities = images_dictionary[image_id]['vulnerabilities']
                    else:
                        vulnerabilities = []
                    cluster = container['info'].get('cluster', "")
                    namespace = container['info'].get('namespace', "")
                    for vulnerability in vulnerabilities:
                        if pc_api.debug:
                            print("#########################################################################")
                            print(json.dumps(vulnerability, indent=4))
                        package_name = vulnerability.get('packageName', "")
                        package_version = vulnerability.get('packageVersion', "")
                        package_path = ""
                        package_license = ""
                        package_key = package_name + package_version
                        if package_key in packages_dictionary:
                            package_info    = packages_dictionary[package_key]
                            package_path    = package_info.get('path', "")
                            package_license = package_info.get('license', "")
                        published_date = datetime_or_empty(vulnerability['published'])
                        fix_date       = datetime_or_empty(vulnerability['fixDate'])
                        # TODO_LAYER
                        # TODO_GRACEPERIODDAYS image? gracePeriodDays
                        # TODO_RISK_FACTORS vulnerability riskFactors array
                        # TODO_TAGS container? labels array
                        # TODO_CONTAINERS ?
                        # TODO_CUSTOM_LABELS container? labels array
                        # TODO_BINARIES vulnerability binaryPkgs array
                        # TODO_COLLECTIONS container? collections array
                        # TODO_DIGEST image? repoDigests
                        # TODO_APPS ?
                        # pylint: disable=line-too-long
                        # Registry,Repository,Tag,Id,Distro,Hosts,Layer,CVE ID,Compliance ID,Type,Severity,Packages,Source Package,Package Version,Package License,CVSS,Fix Status,Fix Date,Grace Days,Risk Factors,Vulnerability Tags,Description,Cause,Containers,Custom Labels,Published,Discovered,Binaries,Clusters,Namespaces,Collections,Digest,Vulnerability Link,Apps,Package Path
                        line = [image['repoTag']['registry'], image['repoTag']['repo'], image['repoTag']['tag'], image_id, image['distro'],host_name,"TODO_LAYER", vulnerability['cve'], vulnerability['templates'], image['type'], vulnerability['severity'], vulnerability['packageName'], "TODO_SOURCE_PACKAGE", vulnerability['packageVersion'], package_license, vulnerability['cvss'], vulnerability['status'], fix_date, "TODO_GRACEPERIODDAYS", "TODO_RISK_FACTORS", "TODO_TAGS", vulnerability['description'], vulnerability['cause'], "TODO_CONTAINERS", "TODO_CUSTOM_LABELS", published_date, vulnerability['discovered'], "TODO_BINARIES", cluster, namespace, "TODO_COLLECTIONS", "TODO_DIGEST", vulnerability['link'], "TODO_APPS", package_path]
                        writer.writerow(line)
                        if pc_api.debug:
                            print("#########################################################################")
                            print(line)

print("* Vulnerabilities Exported")
print()
