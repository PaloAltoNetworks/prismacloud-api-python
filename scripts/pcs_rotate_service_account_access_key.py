""" Rotate (replace) a Service Account Access Key """

import re
import time

from pc_lib import pc_api, pc_utility

# --Configuration-- #

DEFAULT_DAYS = 0

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--days',
    type=int,
    default=DEFAULT_DAYS,
    help=f'(Optional) - Expiration in days from now, with zero equaling no expiration date. (Default: {DEFAULT_DAYS})')
parser.add_argument(
    'base_name',
    type=str,
    help='(Required) - Base name (not including a version suffix) of the Access Key to rotate')
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Helpers-- #

# Identify a matching access key.

def matching_access_key(access_key_name, base_name):
    access_key_name_lower = access_key_name.lower()
    base_name_lower = base_name.lower()
    # Full match.
    if access_key_name_lower == base_name_lower:
        return True
    # Base name match.
    result = re.search(r'(.+) v(\d+)$', access_key_name)
    if result:
        access_key_base_name_lower = result.group(1).lower()
        if access_key_base_name_lower == base_name_lower:
            return True
    # No match.
    return False

# Identify an access key version number.

def current_version(access_key_name):
    result = re.search(r'(.+) v(\d+)$', access_key_name)
    if result:
        return int(result.group(2))
    return 0

# --Main-- #

current_user = pc_api.current_user()

access_keys_list = pc_api.access_keys_list_read()

matching_access_keys = []
for access_key in sorted(access_keys_list, key=lambda item: item['name']):
    if matching_access_key(access_key['name'], args.base_name):
        matching_access_keys.append(access_key)

if len(matching_access_keys) == 0:
    pc_utility.error_and_exit(500, 'Access Key Not Found')
elif len(matching_access_keys) == 1:
    previous_access_key = None
    current_access_key  = matching_access_keys[0]
elif len(matching_access_keys) == 2:
    previous_access_key = matching_access_keys[0]
    current_access_key  = matching_access_keys[1]
else:
    pc_utility.error_and_exit(500, 'Base name not unique: matches more than two Access Keys')

# Safeguards.

if current_access_key['id'].lower() == pc_api.username.lower():
    pc_utility.error_and_exit(500, 'This script cannot rotate its own Access Key')

if previous_access_key and previous_access_key['id'].lower() == pc_api.username.lower():
    pc_utility.error_and_exit(500, 'This script cannot rotate its own Access Key')

if current_access_key['username'].lower() == current_user['email'].lower():
    pc_utility.error_and_exit(500, 'This script can only rotate a Service Account Access Key')

if previous_access_key and previous_access_key['username'].lower() == current_user['email'].lower():
    pc_utility.error_and_exit(500, 'This script can only rotate a Service Account Access Key')

# No expiration, or the specified expiration as a timestamp.

if args.days == 0:
    expires = args.days
else:
    expires = round(time.time() * 1000) + (86400000 * args.days)

# Increment the version number.

version = current_version(current_access_key['name']) + 1
name_and_version = '%s v%s' % (args.base_name, version)

next_access_key = {
    'expiresOn':          expires,
    'name':               name_and_version,
    'serviceAccountName': current_access_key['username'],
}

if previous_access_key:
    pc_api.access_key_delete(previous_access_key['id'])

new_access_key = pc_api.access_key_create(next_access_key)

new_access_key['name'] = name_and_version
print('New Access Key: %s' % new_access_key)
