import json
import os.path
import requests
import sys
import csv

# --Description-- #
# Redlock API Helper library.  Used to contain the API calls and other general useful shared functions.
# --End Description-- #


# --Configuration-- #
# Settings file name
DEFAULT_SETTINGS_FILE_NAME = "rl-settings.conf"
DEFAULT_SETTINGS_FILE_VERSION = 1
# --End Configuration-- #


# --Helper Methods-- #
# Exit handlers
def rl_exit_error(error_code, error_message=None, system_message=None):
    print(error_code)
    if error_message is not None:
        print(error_message)
    if system_message is not None:
        print(system_message)
    sys.exit(1)


def rl_exit_success():
    sys.exit(0)


# Update settings
def rl_settings_upgrade(old_settings):
    rl_exit_error(500, "First version of the settings file - you should not have been able to get here.  Please recreate your settings file as something is wrong.")


# Read in settings
def rl_settings_read(settings_file_name=DEFAULT_SETTINGS_FILE_NAME, settings_file_version=DEFAULT_SETTINGS_FILE_VERSION):
    settings_file_name_and_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), settings_file_name)
    rl_settings = {}
    if os.path.isfile(settings_file_name_and_path):
        try:
            with open(settings_file_name_and_path, 'r') as f:
                rl_settings = json.load(f)
        except Exception as ex:
            rl_exit_error(400, "Error in reading/parsing the rl-settings file.  Please reset the settings using the rl-configure.py utility.", ex)
        if rl_settings['settings_file_version'] == settings_file_version:
            return rl_settings
        elif rl_settings['settings_file_version'] < settings_file_version:
            return rl_settings_upgrade(rl_settings)
        else:
            rl_exit_error(500, "The settings file being used is newer than the utility understands.  "
                            "Please recreate the settings file using the rl-settings.py utility or "
                            "update the Redlock tools in use.")
    else:
        rl_exit_error(400, "Cannot find the rl-settings file.  Please create one using the rl-settings.py utility.")


# Write settings to a file
def rl_settings_write(username, password, customername, settings_file_name=DEFAULT_SETTINGS_FILE_NAME, settings_file_version=DEFAULT_SETTINGS_FILE_VERSION):
    # Write settings file
    new_settings = {}
    new_settings['settings_file_version'] = settings_file_version
    new_settings['username'] = username
    new_settings['password'] = password
    new_settings['customerName'] = customername
    settings_file_name_and_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), settings_file_name)
    try:
        with open(settings_file_name_and_path, 'w') as f:
            json.dump(new_settings, f)
    except Exception as ex:
        rl_exit_error(500, "Failed to create settings file.", ex)


# API Call Function
def rl_call_api(action, api_url, jwt=None, data=None, params=None, count=0):
    headers = {'Content-Type': 'application/json', 'x-redlock-auth': jwt}
    response = requests.request(action, api_url, params=params, headers=headers, data=json.dumps(data))
    # Check for successful API call
    response.raise_for_status()
    try:
        return response.json()
    except ValueError:
        if response.text == '':
            return None
        else:
            rl_exit_error(501, 'The server returned an unexpected server response.')


# Work out login information
def rl_login_get(username, password, customername):
    rl_settings = {}
    if username is None and password is None and customername is None:
        rl_settings = rl_settings_read()
    elif username is None or password is None or customername is None:
        rl_exit_error(400, 'Username (-u), password (-p), and customer name (-c) all required if using overrides.')
    else:
        rl_settings['username'] = username
        rl_settings['password'] = password
        rl_settings['customerName'] = customername
    return rl_settings


# Get JWT for access (Needs data from rl_login_get)
def rl_jwt_get(rl_settings):
    url = "https://api.redlock.io/login"
    action = "POST"
    response = rl_call_api(action, url, data=rl_settings)
    return response['token']


# Load the CSV file into Dict
def rl_file_load_csv(file_name):
    csv_list = []
    with open(file_name, 'rb') as csv_file:
        file_reader = csv.DictReader(csv_file)
        for row in file_reader:
            csv_list.append(row)
    return csv_list
