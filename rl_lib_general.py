import json
import os.path
import sys
import csv

# --Description-- #
# Redlock General Helper library.  Used to contain the general useful shared functions.
# --End Description-- #


# --Configuration-- #
# Settings file name
DEFAULT_SETTINGS_FILE_NAME = "rl-settings.conf"
DEFAULT_SETTINGS_FILE_VERSION = 2
# --End Configuration-- #


# --Helper Methods-- #
# Exit handler (Error)
def rl_exit_error(error_code, error_message=None, system_message=None):
    print(error_code)
    if error_message is not None:
        print(error_message)
    if system_message is not None:
        print(system_message)
    sys.exit(1)


# Exit handler (Success)
def rl_exit_success():
    sys.exit(0)


# Find the correct API Base URL
def rl_find_api_base(ui_base):
    api_base = None
    ui_base_lower = ui_base.lower()
    if ui_base_lower == 'app.redlock.io':
        api_base = 'api.redlock.io'
    elif ui_base_lower == 'app2.redlock.io':
        api_base = 'api2.redlock.io'
    elif ui_base_lower == 'app.eu.redlock.io':
        api_base = 'api.eu.redlock.io'
    else:
        rl_exit_error(400, "API URL Base not found.  Please verify the UI base is accurate.  If it is correct, and you are still getting this message, "
                           "then a new URL was added to the system that this tool does not understand.  Please check for a new version of this tool.")
    return api_base


# Update settings
def rl_settings_upgrade(old_settings):
    if old_settings['settings_file_version'] == 1:
        rl_exit_error(400, "Saved settings file is out of date.  Please re-run the rl-settings.py and update your login settings.")
    else:
        rl_exit_error(500, "Something went wrong.  Settings file appears to be outdated, but this tool cannot understand what version it is.  "
                           "Please recreate the settings file or download the latest version of this tool.")
    return old_settings


# Read in settings
def rl_settings_read(settings_file_name=DEFAULT_SETTINGS_FILE_NAME, settings_file_version=DEFAULT_SETTINGS_FILE_VERSION):
    settings_file_name_and_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), settings_file_name)
    if os.path.isfile(settings_file_name_and_path):
        rl_settings = rl_file_read_json(settings_file_name)
        if rl_settings is None or rl_settings == {}:
            rl_exit_error(500, "The settings file appears to exist, but is empty?  Check the settings file or rerun the rl-configure.py utility.")
        elif rl_settings['settings_file_version'] == settings_file_version:
            return rl_settings
        elif rl_settings['settings_file_version'] < settings_file_version:
            return rl_settings_upgrade(rl_settings)
        else:
            rl_exit_error(500, "The settings file being used is newer than the utility understands.  "
                            "Please recreate the settings file using the rl-configure.py utility or "
                            "update the Redlock tools in use.")
    else:
        rl_exit_error(400, "Cannot find the rl-settings file.  Please create one using the rl-configure.py utility.")


# Write settings to a file
def rl_settings_write(username, password, customername, uiBase,
                      settings_file_name=DEFAULT_SETTINGS_FILE_NAME, settings_file_version=DEFAULT_SETTINGS_FILE_VERSION):
    # Verify API Base is understood
    apiBase = rl_find_api_base(uiBase)

    # Write settings file
    new_settings = {}
    new_settings['settings_file_version'] = settings_file_version
    new_settings['username'] = username
    new_settings['password'] = password
    new_settings['customerName'] = customername
    new_settings['apiBase'] = apiBase
    rl_file_write_json(settings_file_name, new_settings)


# Work out login information
def rl_login_get(username, password, customername, uibase):
    rl_settings = {}
    if username is None and password is None and customername is None and uibase is None:
        rl_settings = rl_settings_read()
    elif username is None or password is None or customername is None or uibase is None:
        rl_exit_error(400, 'Username (-u), password (-p), customer name (-c), and UI URL Base (-url) are all required if using overrides.')
    else:
        rl_settings['username'] = username
        rl_settings['password'] = password
        rl_settings['customerName'] = customername
        rl_settings['apiBase'] = rl_find_api_base(uibase)
    # Add a placeholder for jwt
    rl_settings['jwt'] = None
    return rl_settings


# Load the CSV file into Dict
def rl_file_load_csv(file_name):
    csv_list = []
    with open(file_name, 'rb') as csv_file:
        file_reader = csv.DictReader(csv_file)
        for row in file_reader:
            csv_list.append(row)
    return csv_list


# Write JSON file
def rl_file_write_json(file_name, data_to_write):
    file_name_and_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)
    try:
        with open(file_name_and_path, 'w') as f:
            json.dump(data_to_write, f)
    except Exception as ex:
        rl_exit_error(500, "Failed to write JSON file.", ex)


# Read JSON file into Dict
def rl_file_read_json(file_name):
    json_data = None
    file_name_and_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)
    try:
        with open(file_name_and_path, 'r') as f:
            json_data = json.load(f)
    except Exception as ex:
        rl_exit_error(500, "Failed to read JSON file.  Check the file name?", ex)
    return json_data

