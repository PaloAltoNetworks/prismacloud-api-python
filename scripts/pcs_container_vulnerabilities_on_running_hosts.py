""" Get Vulnerabilities in Containers (Deployed Images) on Recently  Running Hosts """

import csv
import datetime

import dateutil.parser as date_parser
from dateutil import tz

# pylint: disable=import-error
from prismacloudapi import pc_api, pc_utility

# --Configuration-- #

DEFAULT_FILE_NAME = 'vulnerabilities.csv'
DEFAULT_HOURS = 24

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--csv_file_name',
    type=str,
    default=DEFAULT_FILE_NAME,
    help="(Optional) - Export to the given file name. (Default %s)" % DEFAULT_FILE_NAME)
parser.add_argument(
    '--hours',
    type=int,
    default=DEFAULT_HOURS,
    help="(Optional) - Number of hours for a container host to be considered online. (Default %s)" % DEFAULT_HOURS)
parser.add_argument(
    '--multiples',
    type=bool,
    choices=[True, False],
    default=False,
    help="(Optional) - Multiple hosts are running hosts."
)
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)
pc_api.validate_api_compute()

# --Helpers-- #

# TODO: Validate Date Comparison
def recent(datetime_string, delta_hours):
    if delta_hours == 0:
        return True
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

print(hosts, file=open('hosts.txt', 'w'))

hosts_dictionary = {}
for host in hosts:
    # _id or hostname ?
    hosts_dictionary[host['_id']] = host

# https://prisma.pan.dev/api/cloud/cwpp/images#operation/get-images
print('Getting Deployed Images (please wait) ...', end='')
result = pc_api.execute_compute('GET', 'api/v1/images/download?', query_params={'filterBaseImage': 'true'})
print(result, file=open('temp.csv', 'w'))
print(' done.')
print()

images = pc_utility.read_csv_file_text('temp.csv')
headers = images[0].keys()

print("* Exporting Vulnerabilities (please wait) ...")

# TODO: Validate line breaks in fields.
with open(args.csv_file_name, 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for image in images:
        if 'Hosts' in image:
            if image['Hosts'].isnumeric():
                if args.multiples:
                    writer.writerow(image.values())
                else:
                    print("Skipping Container: Multiple Parent Hosts. ID: (%s)" % (image['Id']))
                continue
            if image['Hosts'] in hosts_dictionary:
                host = hosts_dictionary[image['Hosts']]
                if recent(host['scanTime'], args.hours):
                    writer.writerow(image.values())
                else:
                    print("Skipping Container: Parent Host (%s) Last Scan Time: (%s) older than (%s) Hours" % (image['Hosts'], host['scanTime'], args.hours))
            else:
                print("Skipping Container: Parent Host (%s) not found in Hosts. ID: (%s)" % (image['Hosts'], image['Id']))
        else:
            print("Skipping Container: Parent Host not defined in Deployed Images. ID: (%s)" % (image['Id']))

print("* Vulnerabilities Exported")
print()
print("Saved to: %s" % args.csv_file_name)
print()
