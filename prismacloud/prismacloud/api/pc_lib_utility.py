""" Prisma Cloud Utility Class """

from __future__ import print_function

import argparse
import csv
import json
import os
import sys

from update_checker import UpdateChecker
from .version import version as api_version

try:
    # pylint: disable=redefined-builtin
    input = raw_input
except NameError:
    pass

# --Description-- #

# Prisma Cloud Helper library.

# --Helper Methods-- #

class PrismaCloudUtility():
    """ Prisma Cloud Utility Class """

    CONFIG_DIRECTORY = os.path.join(os.environ['HOME'], '.prismacloud')
    DEFAULT_CONFIG_FILE = os.path.join(CONFIG_DIRECTORY, 'credentials.json')

    @classmethod
    def package_version_check(cls, package_name='prismacloud-api'):
        package_version_message = 'version: %s' % api_version
        checker = UpdateChecker()
        result = checker.check(package_name, api_version)
        if result:
            package_version_message = "version update available: %s -> %s\nrun 'pip3 install --upgrade %s' to update" % (api_version, result.available_version, package_name)
        return package_version_message

    # Default command line arguments.

    def get_arg_parser(self):
        get_arg_parser = argparse.ArgumentParser()
        get_arg_parser.add_argument(
            '-u',
            '--username',
            type=str,
            help='(Required) - Prisma Cloud CSPM Access Key (or Compute Username)')
        get_arg_parser.add_argument(
            '-p',
            '--password',
            type=str,
            help='(Required) - Prisma Cloud CSPM Secret Key (or Compute Password)')
        get_arg_parser.add_argument(
            '--api',
            '--api_cspm',
            '--api-cspm',
            default='',
            type=str,
            help='(Optional) - Prisma Cloud CSPM API/UI URL')
        get_arg_parser.add_argument(
            '--api_compute',
            '--api-compute',
            type=str,
            default='',
            help='(Optional with CSPM) Prisma Cloud Compute API/UI URL')
        get_arg_parser.add_argument(
            '--ca_bundle',
            '--ca_certificate',
            '--ca-certificate',
            default='',
            type=str,
            help='(Optional) - Custom CA (bundle) file')
        get_arg_parser.add_argument(
            '-c',
            '--config_file',
            '--config-file',
            '--conf_file',
            '--conf-file',
            default=None,
            type=str,
            help='(Optional) - Configuration file (by default: %s)' % self.DEFAULT_CONFIG_FILE)
        get_arg_parser.add_argument(
           '-y',
           '--yes',
            action='store_true',
            help='(Optional) - Do not prompt for verification.')
        get_arg_parser.add_argument(
           '-d',
           '--debug',
            action='store_true',
            help='(Optional) - Output debugging information.')
        get_arg_parser.epilog=self.package_version_check()
        return get_arg_parser

    # Read or write settings.

    def configure(self, args):
        print('Configuration File Name:')
        if args.config_file is None:
            print(self.DEFAULT_CONFIG_FILE)
        else:
            print(args.config_file)
        print()
        if args.username is None and args.password is None:
            settings = self.read_settings_file(args.config_file)
            self.print_settings_file(settings)
        elif args.api != '' or args.api_compute != '':
            self.write_settings_file(args)
            print('Settings saved.')
        else:
            print('Please specify a CSPM Access Key / Compute Username (-u / --username), CSPM Secret Key / Compute Password (-p / --password), and API/UI URL (--api or --api_compute) to save your configuration.')
            print()
            print('Please specify nothing, other than an optional (--config_file), to view your current configuration.')
        print()

    # Get settings from the command-line and/or settings file.

    def get_settings(self, args):
        settings = {}
        # Verify that there are enough command-line settings to continue, otherwise read the settings file.
        if (args.username is None or args.password is None) or (args.api == '' and args.api_compute == ''):
            settings = self.read_settings_file(args.config_file)
        # Command-line settings take precedence over the settings file.
        if args.username:
            settings['username'] = args.username
        if args.password:
            settings['password'] = args.password
        if args.api != '':
            settings['api'] = args.api
        if args.api_compute != '':
            settings['api_compute'] = args.api_compute
        if args.ca_bundle != '':
            settings['ca_bundle'] = args.ca_bundle
        # Normalize API URLs.
        settings['api']         = self.normalize_api(settings['api'])
        settings['api_compute'] = self.normalize_api_compute(settings['api_compute'])
        # The 'ca_bundle' setting can be a boolean or a string path to a file, as per the 'verify' parameter of requests.request().
        if settings['ca_bundle'] == 'True' or settings['ca_bundle'] == '':
            settings['ca_bundle'] = True
        if settings['ca_bundle'] == 'False':
            settings['ca_bundle'] = False
        # Verify that there are enough settings to continue.
        if settings['username'] is None or settings['password'] is None:
            self.error_and_exit(400, 'Both (--username) and (--password) are required.')
        if settings['api'] == '' and settings['api_compute'] == '':
            self.error_and_exit(400, 'One of API (--api) or API Compute (--api_compute) are required.')
        # Debugging.
        settings['debug'] = args.debug
        return settings

    # Read settings.

    def read_settings_file(self, settings_file_name=None):
        settings_file_name = self.specified_or_default_settings_file(settings_file_name)
        if not os.path.exists(settings_file_name):
            self.error_and_exit(400, 'Cannot open the settings file (%s).\nPlease run pcs_configure.py to create a file, or specify one via (--config_file).' % settings_file_name)
        settings = self.read_json_file(settings_file_name)
        if not settings:
            self.error_and_exit(500, 'Cannot read the settings file.\nPlease run pcs_configure.py to create a new file.')
        # Older settings that have been renamed in newer settings files.
        if 'apiBase' in settings:
            # Do not overwrite the newer setting with the older setting.
            if 'api' not in settings:
                settings['api'] = settings['apiBase']
            del settings['apiBase']
        # Map settings from prismacloud-cli to prismacloud-api.
        if 'access_key_id' in settings:
            settings['username'] = settings['access_key_id']
        if 'secret_key' in settings:
            settings['password'] = settings['secret_key']
        if 'api_endpoint' in settings:
            settings['api'] = settings['api_endpoint']
        if 'pcc_api_endpoint' in settings:
            settings['api_compute'] = settings['pcc_api_endpoint']
        # Newer settings that may not be present in older settings files.
        if 'api' not in settings:
            settings['api'] = ''
        if 'api_compute' not in settings:
            settings['api_compute'] = ''
        if 'ca_bundle' not in settings:
            settings['ca_bundle'] = ''
        return settings

    # Write settings.

    def write_settings_file(self, args):
        settings_file_name = self.specified_or_default_settings_file(args.config_file)
        if not os.path.exists(self.CONFIG_DIRECTORY):
            os.makedirs(self.CONFIG_DIRECTORY)
        settings = {}
        settings['api']         = self.normalize_api(args.api)
        settings['api_compute'] = self.normalize_api_compute(args.api_compute)
        settings['username']    = args.username
        settings['password']    = args.password
        settings['ca_bundle']   = args.ca_bundle
        self.write_json_file(settings_file_name, settings, pretty=True)

    # Output settings.

    @classmethod
    def print_settings_file(cls, settings):
        print('Settings:')
        print()
        if settings['api'] is not None:
            print('Prisma Cloud CSPM API/UI URL:')
            print(settings['api'])
            print()
        if settings['api_compute'] is not None:
            print('Prisma Cloud Compute API/UI URL:')
            print(settings['api_compute'])
            print()
        if settings['username'] is not None:
            print('Prisma Cloud CSPM Access Key (or Compute Username):')
            print(settings['username'])
            print()
        if settings['password'] is not None:
            print('Prisma Cloud CSPM Secret Key (or Compute Password):')
            print(settings['password'])
            print()
        if settings['ca_bundle'] is not None:
            print('Custom CA (bundle) file:')
            print(settings['ca_bundle'])

    # Return the user-specified settings file, or the default settings file.

    def specified_or_default_settings_file(self, settings_file_name=None):
        # Default to the default settings file name and path.
        settings_file_name_and_path = self.DEFAULT_CONFIG_FILE
        if settings_file_name:
            if os.path.sep in settings_file_name:
                # Using the specified settings file name and path verbatim.
                settings_file_name_and_path = settings_file_name
            else:
                # Using the specified file name, in the configuration directory.
                settings_file_name_and_path = os.path.join(self.CONFIG_DIRECTORY, settings_file_name)
        return settings_file_name_and_path

    # Normalize API/UI URL.

    @classmethod
    def normalize_api(cls, api):
        if not api:
            return ''
        api = api.lower()
        api = api.replace('app', 'api')
        api = api.replace('redlock', 'prismacloud')
        api = api.replace('http://', '')
        api = api.replace('https://', '')
        api = api.rstrip('/')
        return api

    # Normalize Compute API/UI URL.

    @classmethod
    def normalize_api_compute(cls, api_compute):
        if not api_compute:
            return ''
        api_compute = api_compute.lower()
        api_compute = api_compute.replace('http://', '')
        api_compute = api_compute.replace('https://', '')
        api_compute = api_compute.rstrip('/')
        return api_compute

    # Double-check action.

    def prompt_for_verification_to_continue(self, args):
        # Only prompt if an interactive shell is detected
        if os.isatty(sys.stdout.fileno()):
            if not args.yes:
                print()
                print('Ready to execute commands against your Prisma Cloud tenant ...')
                verification_response = str(input('Would you like to continue (y or yes)? '))
                continue_response = {'yes', 'y'}
                print()
                if verification_response not in continue_response:
                    self.error_and_exit(400, 'Exiting ...')

    # Load a CSV file into a Dictionary (binary).

    @classmethod
    def read_csv_file(cls, file_name):
        csv_list = []
        with open(file_name, 'rb') as csv_file:
            file_reader = csv.DictReader(csv_file)
            for row in file_reader:
                csv_list.append(row)
        return csv_list

    # Load a CSV file into Dictionary (text).

    @classmethod
    def read_csv_file_text(cls, file_name):
        csv_list = []
        with open(file_name, 'r') as csv_file:
            file_reader = csv.DictReader(csv_file)
            for row in file_reader:
                csv_list.append(row)
        return csv_list

    # Read JSON file into Dictionary.

    def read_json_file(self, file_name):
        json_data = None
        file_name_and_path = os.path.join(os.getcwd(), file_name)
        try:
            with open(file_name_and_path, 'r') as json_file:
                json_data = json.load(json_file)
        # pylint: disable=broad-except
        except Exception as ex:
            self.error_and_exit(500, 'Failed to read JSON file.', ex)
        return json_data

    # Write Dictionary to JSON file.

    def write_json_file(self, file_name, data_to_write, pretty=False):
        file_name_and_path = os.path.join(os.getcwd(), file_name)
        try:
            if pretty:
                pretty_data_to_write = json.dumps(data_to_write, indent=4, separators=(', ', ': '))
                with open(file_name_and_path, 'w') as json_file:
                    json_file.write(pretty_data_to_write)
            else:
                with open(file_name_and_path, 'w') as json_file:
                    json.dump(data_to_write, json_file)
        # pylint: disable=broad-except
        except Exception as ex:
            self.error_and_exit(500, 'Failed to write JSON file.', ex)

    # Search list for a field with a certain value and return another field value from that object.

    @classmethod
    def search_list_value(cls, list_to_search, field_to_search, field_to_return, search_value):
        item_to_return = None
        for source_item in list_to_search:
            if field_to_search in source_item:
                if source_item[field_to_search] == search_value:
                    item_to_return = source_item[field_to_return]
                    break
        return item_to_return

    # Search list for a field with a certain value and return another field value from that object (case insensitive).

    @classmethod
    def search_list_value_lower(cls, list_to_search, field_to_search, field_to_return, search_value):
        item_to_return = None
        search_value = search_value.lower()
        for source_item in list_to_search:
            if field_to_search in source_item:
                if source_item[field_to_search].lower() == search_value:
                    item_to_return = source_item[field_to_return]
                    break
        return item_to_return

    # Search list for a field with a certain value and return the entire object.

    @classmethod
    def search_list_object(cls, list_to_search, field_to_search, search_value):
        object_to_return = None
        for source_item in list_to_search:
            if field_to_search in source_item:
                if source_item[field_to_search] == search_value:
                    object_to_return = source_item
                    break
        return object_to_return

    # Search list for a field with a certain value and return the entire object (case insensitive).

    @classmethod
    def search_list_object_lower(cls, list_to_search, field_to_search, search_value):
        object_to_return = None
        search_value = search_value.lower()
        for source_item in list_to_search:
            if field_to_search in source_item:
                if source_item[field_to_search].lower() == search_value:
                    object_to_return = source_item
                    break
        return object_to_return

    # Search list for a field with a certain value and return a list of all objects that match.

    @classmethod
    def search_list_list(cls, list_to_search, field_to_search, search_value):
        object_list_to_return = []
        for source_item in list_to_search:
            if field_to_search in source_item:
                if source_item[field_to_search] == search_value:
                    object_list_to_return.append(source_item)
                    break
        return object_list_to_return

    # Search list for a field with a certain value and return a list of all objects that match (case insensitive).

    @classmethod
    def search_list_list_lower(cls, list_to_search, field_to_search, search_value):
        object_list_to_return = []
        search_value = search_value.lower()
        for source_item in list_to_search:
            if field_to_search in source_item:
                if source_item[field_to_search].lower() == search_value:
                    object_list_to_return.append(source_item)
                    break
        return object_list_to_return

    # Exit handler (Error).

    @classmethod
    def error_and_exit(cls, error_code, error_message=None, system_message=None):
        print()
        print()
        print('Status Code: %s' % error_code)
        if error_message is not None:
            print(error_message)
        if system_message is not None:
            print(system_message)
        print()
        sys.exit(1)

    # Exit handler (Success).

    @classmethod
    def success_exit(cls):
        sys.exit(0)
