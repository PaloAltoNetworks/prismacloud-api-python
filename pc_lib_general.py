import argparse
import csv
import json
import os.path
import sys

# --Description-- #

# Prisma Cloud General Helper library.

# --Configuration-- #

DEFAULT_SETTINGS_FILE_NAME    = 'pc-settings.conf'
DEFAULT_SETTINGS_FILE_VERSION = 4

# --Helper Methods-- #

# Parse command line arguments.

def pc_arg_parser_defaults():
    pc_arg_parser_defaults = argparse.ArgumentParser()
    pc_arg_parser_defaults.add_argument(
        '-u',
        '--username',
        type=str,
        help='(Required) - Prisma Cloud API Access Key.')
    pc_arg_parser_defaults.add_argument(
        '-p',
        '--password',
        type=str,
        help='(Required) - Prisma Cloud API Secret Key.')
    pc_arg_parser_defaults.add_argument(
        '-url',
        '--uiurl',
        type=str,
        help='(Required) - Prisma Cloud API/UI Base URL')
    pc_arg_parser_defaults.add_argument(
        '--ca_bundle',
        default=None,
        type=str,
        help='(Optional) - Custom CA (bundle) file')
    pc_arg_parser_defaults.add_argument(
        '-conf_file',
        '--config_file',
        default=None,
        type=str,
        help='(Optional) - Prisma Cloud API configuration settings file (by default: %s).' % DEFAULT_SETTINGS_FILE_NAME)
    pc_arg_parser_defaults.add_argument(
       '-y',
       '--yes',
        action='store_true',
        help='(Optional) - Do not prompt for verification.')
    return pc_arg_parser_defaults

# Get settings from command-line or settings file.

def pc_settings_get(args):
    pc_settings = {}
    if args.username is None and args.password is None and args.uiurl is None:
        pc_settings = pc_settings_file_read(args.config_file)
        if 'ca_bundle' not in pc_settings:
            pc_settings['ca_bundle'] = None
    elif args.username is None or args.password is None or args.uiurl is None:
        pc_exit_error(400, 'Access Key (--username), Secret Key (--password), and API/UI Base URL (--uiurl) are all required.')
    else:
        pc_settings['apiBase']   = pc_normalize_api_base(args.uiurl)
        pc_settings['username']  = args.username
        pc_settings['password']  = args.password
        pc_settings['ca_bundle'] = args.ca_bundle
    return pc_settings

# Read settings.

def pc_settings_file_read(settings_file_name=None):
    settings_file_name = user_or_default_settings_file(settings_file_name)
    if not os.path.isfile(settings_file_name):
        pc_exit_error(400, 'Cannot find the settings file. Please run pc-configure.py.')
    pc_settings = pc_file_read_json(settings_file_name)
    if not pc_settings:
        pc_exit_error(500, 'The settings file exists, but cannot be read. Please run pc-configure.py.')
    if pc_settings['settings_file_version'] != DEFAULT_SETTINGS_FILE_VERSION:
        pc_exit_error(500, 'The settings file appears to be out-of-date. Please rerun pc-configure.py, and/or download the latest version of these scripts.')
    return pc_settings

# Write settings.

def pc_settings_file_write(args):
    settings_file_name = user_or_default_settings_file(args.config_file)
    pc_settings = {}
    pc_settings['settings_file_version'] = DEFAULT_SETTINGS_FILE_VERSION
    pc_settings['apiBase']   = pc_normalize_api_base(args.uiurl)
    pc_settings['username']  = args.username
    pc_settings['password']  = args.password
    pc_settings['ca_bundle'] = args.ca_bundle
    pc_file_write_json(settings_file_name, pc_settings)

# Return user-specified settings file, or the default settings file.

def user_or_default_settings_file(settings_file_name=DEFAULT_SETTINGS_FILE_NAME):
    if settings_file_name == DEFAULT_SETTINGS_FILE_NAME:
        # Using the default file name, in the same directory as the script.
        settings_file_name_and_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), settings_file_name)
        # TBD:
        # If the default file name does not exist in the same directory as the script, use the default file name in the home directory.
        # if not os.path.isfile(settings_file_name_and_path):
        #    settings_file_name_and_path = os.path.join(os.path.expanduser('~'), settings_file_name)
    else:
        # Using the specified file name.
        if os.path.sep in settings_file_name:
            # Use the specified file name verbatim, as it is a file path.
            settings_file_name_and_path = settings_file_name
        else:
            # Use the specified file name, in the same directory as the script.
            settings_file_name_and_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), settings_file_name)
    return settings_file_name_and_path

# Normalize API/UI Base URL.

def pc_normalize_api_base(ui_base):
    ui_base_lower = ui_base.lower()
    ui_base_lower = ui_base_lower.replace('app', 'api')
    ui_base_lower = ui_base_lower.replace('redlock', 'prismacloud')
    return ui_base_lower

# Double-check action.

def prompt_for_verification_to_continue(args):
    if not args.yes:
        print()
        print('Ready to execute commands against your Prisma Cloud tenant ...')
        verification_response = str(input('Would you like to continue (y or yes)? '))
        continue_response = {'yes', 'y'}
        print()
        if verification_response not in continue_response:
            pc_exit_error(400, 'Exiting ...')

# Exit handler (Error).

def pc_exit_error(error_code, error_message=None, system_message=None):
    print('Status Code: %s' % error_code)
    if error_message is not None:
        print(error_message)
    if system_message is not None:
        print(system_message)
    sys.exit(1)

# Exit handler (Success).

def pc_exit_success():
    sys.exit(0)

# Load a CSV file into a Dictionary (binary).

def pc_file_load_csv(file_name):
    csv_list = []
    with open(file_name, 'rb') as csv_file:
        file_reader = csv.DictReader(csv_file)
        for row in file_reader:
            csv_list.append(row)
    return csv_list

# Load a CSV file into Dictionary (text).

def pc_file_load_csv_text(file_name):
    csv_list = []
    with open(file_name, 'r') as csv_file:
        file_reader = csv.DictReader(csv_file)
        for row in file_reader:
            csv_list.append(row)
    return csv_list

# Write Dictionary to JSON file.

def pc_file_write_json(file_name, data_to_write):
    file_name_and_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)
    try:
        with open(file_name_and_path, 'w') as f:
            json.dump(data_to_write, f)
    except Exception as ex:
        pc_exit_error(500, 'Failed to write JSON file.', ex)

# Read JSON file into Dictionary.

def pc_file_read_json(file_name):
    json_data = None
    file_name_and_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)
    try:
        with open(file_name_and_path, 'r') as f:
            json_data = json.load(f)
    except Exception as ex:
        pc_exit_error(500, 'Failed to read JSON file.', ex)
    return json_data

# Search list for a field with a certain value and return another field value from that object.

def search_list_value(list_to_search, field_to_search, field_to_return, search_value):
    item_to_return = None
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search] == search_value:
                item_to_return = source_item[field_to_return]
                break
    return item_to_return

# Search list for a field with a certain value and return another field value from that object (case insensitive).

def search_list_value_lower(list_to_search, field_to_search, field_to_return, search_value):
    item_to_return = None
    search_value = search_value.lower()
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search].lower() == search_value:
                item_to_return = source_item[field_to_return]
                break
    return item_to_return

# Search list for a field with a certain value and return the entire object.

def search_list_object(list_to_search, field_to_search, search_value):
    object_to_return = None
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search] == search_value:
                object_to_return = source_item
                break
    return object_to_return

# Search list for a field with a certain value and return the entire object (case insensitive).

def search_list_object_lower(list_to_search, field_to_search, search_value):
    object_to_return = None
    search_value = search_value.lower()
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search].lower() == search_value:
                object_to_return = source_item
                break
    return object_to_return

# Search list for a field with a certain value and return a list of all objects that match.

def search_list_list(list_to_search, field_to_search, search_value):
    object_list_to_return = []
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search] == search_value:
                object_list_to_return.append(source_item)
                break
    return object_list_to_return

# Search list for a field with a certain value and return a list of all objects that match (case insensitive).

def search_list_list_lower(list_to_search, field_to_search, search_value):
    object_list_to_return = []
    search_value = search_value.lower()
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search].lower() == search_value:
                object_list_to_return.append(source_item)
                break
    return object_list_to_return
    