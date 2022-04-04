""" Rotate (replace) a Service Account Access Key """

import re
import time

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

DEFAULT_DAYS = 0

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--days',
    type=int,
    default=DEFAULT_DAYS,
    help=f'(Optional) - Expiration in days from now, with 0 equaling no expiration date. (Default: {DEFAULT_DAYS})')
parser.add_argument(
    'base_key_name',
    type=str,
    help="(Required) - Access Key name (not including a ' vN' version suffix) of the Access Key to rotate")
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Helpers-- #

# Identify a matching access key by name.

def matching_access_key(access_key_name, base_key_name):
    access_key_name_lower = access_key_name.lower()
    base_key_name_lower = base_key_name.lower()
    # Exact name match.
    if access_key_name_lower == base_key_name_lower:
        return True
    # Name with version match.
    matches = re.search(r'(.+) v(\d+)$', access_key_name)
    if matches:
        access_key_base_name_lower = matches.group(1).lower()
        if access_key_base_name_lower == base_key_name_lower:
            return True
    # No match.
    return False

# Identify an access key version number by name.

def get_current_version(access_key_name):
    matches = re.search(r'(.+) v(\d+)$', access_key_name)
    if matches:
        return int(matches.group(2))
    return 0

# --Main-- #

# Queries.

current_user = pc_api.current_user()

access_keys_list = pc_api.access_keys_list_read()

# Selection.

matching_access_keys = []
for access_key in access_keys_list:
    if matching_access_key(access_key['name'], args.base_key_name):
        matching_access_keys.append(access_key)

if len(matching_access_keys) == 0:
    pc_utility.error_and_exit(500, 'Access Key Not Found')

if len(matching_access_keys) == 1:
    previous_access_key = None
    current_access_key  = matching_access_keys[0]
elif len(matching_access_keys) == 2:
    matching_access_keys = sorted(matching_access_keys, key=lambda item: get_current_version(item['name']))
    previous_access_key = matching_access_keys[0]
    current_access_key  = matching_access_keys[1]
else:
    pc_utility.error_and_exit(500, 'Access Key not unique: matches more than two Access Keys')

# Safeguards.

if current_access_key['id'].lower() == pc_api.username.lower():
    pc_utility.error_and_exit(500, 'This script cannot rotate its own Access Key')

if previous_access_key and previous_access_key['id'].lower() == pc_api.username.lower():
    pc_utility.error_and_exit(500, 'This script cannot rotate its own Access Key')

if current_access_key['username'].lower() == current_user['email'].lower():
    pc_utility.error_and_exit(500, 'This script can only rotate Service Account Access Keys')

if previous_access_key and previous_access_key['username'].lower() == current_user['email'].lower():
    pc_utility.error_and_exit(500, 'This script can only rotate Service Account Access Keys')

# Expiration: none, or the specified expiration in days as a timestamp.

if args.days == 0:
    expires = args.days
else:
    expires = round(time.time() * 1000) + (86400000 * args.days)

# Increment the version number.

version = get_current_version(current_access_key['name']) + 1
name_and_version = '%s v%s' % (args.base_key_name, version)

next_access_key = {
    'expiresOn':          expires,
    'name':               name_and_version,
    'serviceAccountName': current_access_key['username'],
}

# Delete the previous access key, if it exists.

if previous_access_key:
    result = pc_api.access_key_delete(previous_access_key['id'])

# Create the next access key.

new_access_key = pc_api.access_key_create(next_access_key)

# Output the next access key.

new_access_key['name'] = name_and_version
print('Next Access Key: %s' % new_access_key)
