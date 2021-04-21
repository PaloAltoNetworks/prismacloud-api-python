import argparse
import csv
import json
import os.path
import sys

# --Description-- #

# Prisma Cloud General Helper library.  Used to contain the general useful shared functions.

# --Configuration-- #

DEFAULT_SETTINGS_FILE_NAME = 'pc-settings.conf'
DEFAULT_SETTINGS_FILE_VERSION = 4

# --Helper Methods-- #

# Parse command line arguments.

def pc_arg_parser_defaults():
    pc_arg_parser_defaults = argparse.ArgumentParser(prog='pctoolbox')
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
        '-conf_file',
        '--config_file',
        type=str,
        help='(Optional) - File containing Prisma Cloud API configuration settings (by default: %s).' % DEFAULT_SETTINGS_FILE_NAME)
    pc_arg_parser_defaults.add_argument(
       '-y',
       '--yes',
        action='store_true',
        help='(Optional) - Do not prompt for verification.')
    return pc_arg_parser_defaults

# Exit handler (Error).

def pc_exit_error(error_code, error_message=None, system_message=None):
    print(error_code)
    if error_message is not None:
        print(error_message)
    if system_message is not None:
        print(system_message)
    sys.exit(1)

# Exit handler (Success).

def pc_exit_success():
    sys.exit(0)

# Find the correct API Base URL.

def pc_find_api_base(ui_base):
    api_base = None
    ui_base_lower = ui_base.lower()
    if ui_base_lower in ['app.redlock.io', 'app.prismacloud.io', 'api.redlock.io']:
        api_base = 'api.prismacloud.io'
    elif ui_base_lower in ['app2.redlock.io', 'app2.prismacloud.io', 'api2.redlock.io']:
        api_base = 'api2.prismacloud.io'
    elif ui_base_lower in ['app3.redlock.io', 'app3.prismacloud.io', 'api3.redlock.io']:
        api_base = 'api3.prismacloud.io'
    elif ui_base_lower in ['app4.redlock.io', 'app4.prismacloud.io', 'api4.redlock.io']:
        api_base = 'api4.prismacloud.io'
    elif ui_base_lower in ['app.eu.redlock.io', 'app.eu.prismacloud.io', 'api.eu.redlock.io']:
        api_base = 'api.eu.prismacloud.io'
    elif ui_base_lower in ['app2.eu.redlock.io', 'app2.eu.prismacloud.io', 'api2.eu.redlock.io']:
        api_base = 'api2.eu.prismacloud.io'
    elif ui_base_lower in ['app.anz.redlock.io', 'app.anz.prismacloud.io', 'api.anz.redlock.io']:
        api_base = 'api.anz.prismacloud.io'
    elif ui_base_lower in ['app.gov.redlock.io', 'app.gov.prismacloud.io', 'api.gov.redlock.io']:
        api_base = 'api.gov.prismacloud.io'
    elif ui_base_lower in ['api.prismacloud.io', 'api2.prismacloud.io', 'api3.prismacloud.io', 'api4.prismacloud.io', 'api.eu.prismacloud.io', 'api2.eu.prismacloud.io', 'api.anz.prismacloud.io', 'api.gov.prismacloud.io']:
        api_base = ui_base_lower
    else:
        pc_exit_error(400, 'Prisma Cloud API/UI Base URL not found. Please verify. If you still receive this error, please download the latest version of these scripts.')
    return api_base

# Use user-specified settings file, or the default settings file.

def user_or_default_settings_file(settings_file_name=None):
    if settings_file_name is None:
        settings_file_name = DEFAULT_SETTINGS_FILE_NAME
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
            # Use the specified file name verbatim, if it is a file path.
            settings_file_name_and_path = settings_file_name
        else:
            # Use the specified file name in the same directory as the script.
            settings_file_name_and_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), settings_file_name)
    return settings_file_name_and_path

# Read settings.

def pc_settings_read(settings_file_name=None, settings_file_version=None):
    settings_file_name = user_or_default_settings_file(settings_file_name)
    if settings_file_version is None:
        settings_file_version = DEFAULT_SETTINGS_FILE_VERSION
    if os.path.isfile(settings_file_name):
        pc_settings = pc_file_read_json(settings_file_name)
        if pc_settings is None or pc_settings == {}:
            pc_exit_error(500, 'The settings file exists, but cannot be read. Please run the configuration script.')
        elif pc_settings['settings_file_version'] == settings_file_version:
            return pc_settings
        elif pc_settings['settings_file_version'] < settings_file_version:
            if pc_settings['settings_file_version'] < DEFAULT_SETTINGS_FILE_VERSION:
                pc_exit_error(400, 'The settings file is out-of-date. Please run the configuration script.')
            else:
                pc_exit_error(500, 'The settings file appears to be out-of-date, but this script cannot determine its version. Please rerun the configuration script, or download the latest version of these scripts.')
        else:
            pc_exit_error(500, 'The settings file version is newer than this script. Please run the configuration script, or download the latest version of these scripts.')
    else:
        pc_exit_error(400, 'Cannot find the settings file. Please run the configuration script.')

# Write settings.

def pc_settings_write(username, password, uiBase, settings_file_name=None, settings_file_version=None):
    settings_file_name = user_or_default_settings_file(settings_file_name)
    if settings_file_version is None:
        settings_file_version = DEFAULT_SETTINGS_FILE_VERSION
    # Verifies API Base is translated
    apiBase = pc_find_api_base(uiBase)
    new_settings = {}
    new_settings['settings_file_version'] = settings_file_version
    new_settings['username'] = username
    new_settings['password'] = password
    new_settings['apiBase']  = apiBase
    pc_file_write_json(settings_file_name, new_settings)

# Login.

def pc_login_get(username, password, uibase, settings_file_name=None):
    pc_settings = {}
    if username is None and password is None and uibase is None:
        pc_settings = pc_settings_read(settings_file_name)
    elif username is None or password is None or uibase is None:
        pc_exit_error(400, 'Access Key (--username), Secret Key (--password), and UI URL Base (--uiurl) are all required.')
    else:
        pc_settings['username'] = username
        pc_settings['password'] = password
        pc_settings['apiBase'] = pc_find_api_base(uibase)
    # Add a placeholder for the JWT.
    pc_settings['jwt'] = None
    return pc_settings

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

# 

def prompt_for_verification_to_continue(yes):
    if not yes:
        print()
        print('Ready to execute commands against your Prisma Cloud tenant.')
        verification_response = str(input('Would you like to continue (y or yes)? '))
        continue_response = {'yes', 'y'}
        print()
        if verification_response not in continue_response:
            pc_exit_error(400, 'Exiting ...')

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
    