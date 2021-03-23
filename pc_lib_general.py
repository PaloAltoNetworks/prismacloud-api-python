import argparse
import json
import os.path
import sys
import csv

# --Description-- #
# Prisma Cloud General Helper library.  Used to contain the general useful shared functions.
# --End Description-- #


# --Configuration-- #
# Settings file name
DEFAULT_SETTINGS_FILE_NAME = "pc-settings.conf"
DEFAULT_SETTINGS_FILE_VERSION = 4
# --End Configuration-- #


# --Helper Methods-- #
# --Parse command line arguments-- #
def pc_arg_parser_defaults():
    pc_arg_parser_defaults = argparse.ArgumentParser(prog='pctoolbox')
    pc_arg_parser_defaults.add_argument(
        '-u',
        '--username',
        type=str,
        help='*Required* - Prisma Cloud API Access Key ID that you want to set to access your Prisma Cloud account.')

    pc_arg_parser_defaults.add_argument(
        '-p',
        '--password',
        type=str,
        help='*Required* - Prisma Cloud API Secret Key that you want to set to access your Prisma Cloud account.')

    pc_arg_parser_defaults.add_argument(
        '-url',
        '--uiurl',
        type=str,
        help='*Required* - Base URL used in the UI for connecting to Prisma Cloud. '
             'Formatted as app.prismacloud.io or app2.prismacloud.io or app.eu.prismacloud.io, etc. '
             'You can also input the api version of the URL if you know it and it will be passed through. ')

    pc_arg_parser_defaults.add_argument(
       '-y',
       '--yes',
        action='store_true',
        help='*Optional* - Override user input for verification (auto answer for yes).')

    return pc_arg_parser_defaults


# Exit handler (Error)
def pc_exit_error(error_code, error_message=None, system_message=None):
    print(error_code)
    if error_message is not None:
        print(error_message)
    if system_message is not None:
        print(system_message)
    sys.exit(1)


# Exit handler (Success)
def pc_exit_success():
    sys.exit(0)


# Find the correct API Base URL
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
    elif ui_base_lower in ['api.prismacloud.io', 'api2.prismacloud.io', 'api3.prismacloud.io', 'api4.prismacloud.io',
                           'api.eu.prismacloud.io', 'api2.eu.prismacloud.io', 'api.anz.prismacloud.io', 'api.gov.prismacloud.io']:
        api_base = ui_base_lower
    else:
        pc_exit_error(400, "API URL Base not found.  Please verify the UI base is accurate.  If it is correct, and you are still getting this message, "
                           "then a new URL was added to the system that this tool does not understand.  Please check for a new version of this tool.")
    return api_base


# Update settings
def pc_settings_upgrade(old_settings):
    if old_settings['settings_file_version'] < DEFAULT_SETTINGS_FILE_VERSION:
        pc_exit_error(400, "Saved settings file is out of date.  Please re-run the pc-settings.py and update your login settings.")
    else:
        pc_exit_error(500, "Something went wrong.  Settings file appears to be outdated, but this tool cannot understand what version it is.  "
                           "Please recreate the settings file or download the latest version of this tool.")
    return old_settings


# Read in settings
def pc_settings_read(settings_file_name=DEFAULT_SETTINGS_FILE_NAME, settings_file_version=DEFAULT_SETTINGS_FILE_VERSION):
    settings_file_name_and_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), settings_file_name)
    if os.path.isfile(settings_file_name_and_path):
        pc_settings = pc_file_read_json(settings_file_name)
        if pc_settings is None or pc_settings == {}:
            pc_exit_error(500, "The settings file appears to exist, but is empty?  Check the settings file or rerun the pc-configure.py utility.")
        elif pc_settings['settings_file_version'] == settings_file_version:
            return pc_settings
        elif pc_settings['settings_file_version'] < settings_file_version:
            return pc_settings_upgrade(pc_settings)
        else:
            pc_exit_error(500, "The settings file being used is newer than the utility understands.  "
                            "Please recreate the settings file using the pc-configure.py utility or "
                            "update the Prisma Cloud tools in use.")
    else:
        pc_exit_error(400, "Cannot find the pc-settings file.  Please create one using the pc-configure.py utility.")


# Write settings to a file
def pc_settings_write(username, password, uiBase,
                      settings_file_name=DEFAULT_SETTINGS_FILE_NAME, settings_file_version=DEFAULT_SETTINGS_FILE_VERSION):
    # Verify API Base is understood
    apiBase = pc_find_api_base(uiBase)

    # Write settings file
    new_settings = {}
    new_settings['settings_file_version'] = settings_file_version
    new_settings['username'] = username
    new_settings['password'] = password
    new_settings['apiBase'] = apiBase
    pc_file_write_json(settings_file_name, new_settings)


# Work out login information
def pc_login_get(username, password, uibase):
    pc_settings = {}
    if username is None and password is None and uibase is None:
        pc_settings = pc_settings_read()
    elif username is None or password is None or uibase is None:
        pc_exit_error(400, 'Access Key ID (--username), Secret Key (--password), and UI URL Base (--uiurl) are all required if using overrides.')
    else:
        pc_settings['username'] = username
        pc_settings['password'] = password
        pc_settings['apiBase'] = pc_find_api_base(uibase)
    # Add a placeholder for jwt
    pc_settings['jwt'] = None
    return pc_settings


# Load the CSV file into Dict
def pc_file_load_csv(file_name):
    csv_list = []
    with open(file_name, 'rb') as csv_file:
        file_reader = csv.DictReader(csv_file)
        for row in file_reader:
            csv_list.append(row)
    return csv_list


# Load the CSV file into Dict (text)
def pc_file_load_csv_text(file_name):
    csv_list = []
    with open(file_name, 'r') as csv_file:
        file_reader = csv.DictReader(csv_file)
        for row in file_reader:
            csv_list.append(row)
    return csv_list


# Write JSON file
def pc_file_write_json(file_name, data_to_write):
    file_name_and_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)
    try:
        with open(file_name_and_path, 'w') as f:
            json.dump(data_to_write, f)
    except Exception as ex:
        pc_exit_error(500, "Failed to write JSON file.", ex)


# Read JSON file into Dict
def pc_file_read_json(file_name):
    json_data = None
    file_name_and_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)
    try:
        with open(file_name_and_path, 'r') as f:
            json_data = json.load(f)
    except Exception as ex:
        pc_exit_error(500, "Failed to read JSON file.  Check the file name?", ex)
    return json_data


# Search list for a field with a certain value and return another field value from that object
def search_list_value(list_to_search, field_to_search, field_to_return, search_value):
    item_to_return = None
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search] == search_value:
                item_to_return = source_item[field_to_return]
                break
    return item_to_return


# Search list for a field with a certain value and return another field value from that object (case insensitive)
def search_list_value_lower(list_to_search, field_to_search, field_to_return, search_value):
    item_to_return = None
    search_value = search_value.lower()
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search].lower() == search_value:
                item_to_return = source_item[field_to_return]
                break
    return item_to_return


# Search list for a field with a certain value and return the entire object
def search_list_object(list_to_search, field_to_search, search_value):
    object_to_return = None
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search] == search_value:
                object_to_return = source_item
                break
    return object_to_return


# Search list for a field with a certain value and return the entire object (case insensitive)
def search_list_object_lower(list_to_search, field_to_search, search_value):
    object_to_return = None
    search_value = search_value.lower()
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search].lower() == search_value:
                object_to_return = source_item
                break
    return object_to_return


# Search list for a field with a certain value and return a list of all objects that match
def search_list_list(list_to_search, field_to_search, search_value):
    object_list_to_return = []
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search] == search_value:
                object_list_to_return.append(source_item)
                break
    return object_list_to_return


# Search list for a field with a certain value and return a list of all objects that match (case insensitive)
def search_list_list_lower(list_to_search, field_to_search, search_value):
    object_list_to_return = []
    search_value = search_value.lower()
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search].lower() == search_value:
                object_list_to_return.append(source_item)
                break
    return object_list_to_return
    