""" Get Vulnerabilities in Containers (Deployed Images) on Recently  Running Hosts """

import csv
import datetime

import dateutil.parser as date_parser
from dateutil import tz

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

# TODO: Validate Date Comparison
def recent(datetime_string, delta_hours=24):
    now = datetime.datetime.now().astimezone(tz.tzlocal())
    dat = date_parser.isoparse(datetime_string).astimezone(tz.tzlocal())
    if now - datetime.timedelta(hours=delta_hours) <= dat <= now:
        return True
    return False

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

hosts_dictionary = {}
for host in hosts:
    hosts_dictionary[host['_id']] = host

# https://prisma.pan.dev/api/cloud/cwpp/images#operation/get-images
print('Getting Deployed Images (please wait) ...', end='')
result = pc_api.execute_compute('GET', 'api/v1/images/download?', query_params={'filterBaseImage': 'true'})
print(' done.')
print()

print(result, file=open('temp.csv', 'w'))
images = pc_utility.read_csv_file_text('temp.csv')
headers = images[0].keys()

print("* Exporting Vulnerabilities (please wait) ...")

# TODO: Validate line breaks in fields.
with open(args.csv_file_name, 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for image in images:
        if 'Hosts' in image:
            host = image['Hosts']
            if image['Hosts'] in hosts_dictionary:
                host = hosts_dictionary[image['Hosts']]
                 # TODO REPLACE WITH ALTERNATIVE TO host['stopped']
                if recent(host['scanTime']):
                    writer.writerow(image.values())
                else:
                    print("Skipping: Last Scan Time: (%s) Host (%s)" % (host['scanTime'], image['Hosts']))

print("* Vulnerabilities Exported")
print()
print("Saved to: %s" % args.csv_file_name)
print()
