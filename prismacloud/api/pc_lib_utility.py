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
            '--name',
            default=os.environ.get('PC_NAME', ''),
            type=str,
            help='(Optional) - Prisma Cloud Tenant (or Compute Console) Name')
        get_arg_parser.add_argument(
            '--url',
            '--api',
            '--api_compute',
            default=os.environ.get('PC_URL', ''),
            type=str,
            help='(Required) - Prisma Cloud Tenant (or Compute Console) URL')
        get_arg_parser.add_argument(
            '-i',
            '--identity',
            '--access_key',
            '--username',
            default=os.environ.get('PC_IDENTITY', ''),
            type=str,
            help='(Required) - Access Key (or Compute Username)')
        get_arg_parser.add_argument(
            '-s',
            '--secret',
            '--secret_key',
            '--password',
            default=os.environ.get('PC_SECRET', ''),
            type=str,
            help='(Required) - Secret Key (or Compute Password)')
        get_arg_parser.add_argument(
            '--verify',
            default=os.environ.get('PC_VERIFY', ''),
            type=str,
            help='(Optional) - SSL Verification. Options: true, false, or the path to a certificate bundle (Default: true)')
        get_arg_parser.add_argument(
           '--logger',
            default=os.environ.get('PC_LOGGER', ''),
            type=str,
            help='(Optional) - TODO: Logger.')
        get_arg_parser.add_argument(
            '-c',
            '--config',
            default=None,
            type=str,
            help='(Optional) - Configuration file (Default: %s)' % self.DEFAULT_CONFIG_FILE)
        get_arg_parser.add_argument(
            '--save',
            action='store_true',
            help='(Optional) - Save configuration file')
        get_arg_parser.add_argument(
           '-y',
           '--yes',
            action='store_true',
            help='(Optional) - Do not prompt for verification')
        get_arg_parser.add_argument(
           '-d',
           '--debug',
            action='store_true',
            help='(Optional) - Output debugging information')
        get_arg_parser.epilog=self.package_version_check()
        return get_arg_parser

    # Read arguments from the command line and/or a settings file.
    # If the command line specifies '--save' then also save command line settings to a settings file,
    # making the get_settings() method name something to refactor.

    def get_settings(self, args=None):
        settings = {}
        # Read the command line arguments, or read a configuration file.
        if isinstance(args, argparse.Namespace):
            # Verify that there are enough command line arguments to continue, otherwise read the settings file.
            if args.url == '' or args.identity == '' or args.secret == '':
                settings = self.read_settings_file(args.config)
            # These command line arguments take precedence over the settings file.
            if args.name != '':
                settings['name'] = args.name
            if args.url != '':
                settings['url'] = args.url
            if args.identity != '':
                settings['identity'] = args.identity
            if args.secret != '':
                settings['secret'] = args.secret
            if args.verify != '':
                settings['verify'] = args.verify
            if args.verify != '':
                settings['logger'] = args.logger
            # These settings are only command line arguments.
            settings['debug'] = args.debug
            settings['yes'] = args.debug
        # No command line arguments provided, read the default settings file.
        else:
            settings = self.read_settings_file()
        settings['url'] = self.normalize_api(settings['url'])
        # The 'verify' setting can be a boolean or a string path to a file, as per the 'verify' parameter of requests.request().
        if settings['verify'].lower() == 'true' or settings['verify'] == '':
            settings['verify'] = True
        elif settings['verify'].lower() == 'false':
            settings['verify'] = False
        # Optionally save command line settings to a settings file.
        if isinstance(args, argparse.Namespace) and args.save:
            self.write_settings_file(args)
            print()
            print('Congifiguration saved to: %s' % args.config)
            print()
        # Verify that there are enough settings to continue.
        if settings['url'] == '' or settings['identity'] == '' or settings['secret'] == '':
            self.error_and_exit(400, 'Settings --url, --identity, and --secret are required to continue.')
        return settings

    # Read settings.

    # pylint: disable=too-many-branches
    def read_settings_file(self, settings_file_name=None):
        settings_file_name = self.specified_or_default_settings_file(settings_file_name)
        if not os.path.exists(settings_file_name):
            self.error_and_exit(400, 'Cannot open the settings file (%s)' % settings_file_name)
        settings = self.read_json_file(settings_file_name)
        if not settings:
            self.error_and_exit(400, 'Cannot read the settings file (%s)' % settings_file_name)
        # Map settings that may be present in older settings files.
        if settings.get('api_endpoint'):
            settings['url'] = settings['api_endpoint']
        if settings.get('pcc_api_endpoint'):
            settings['url'] = settings['pcc_api_endpoint']
        if settings.get('api'):
            settings['url'] = settings.get('api', )
        if settings.get('api_compute'):
            settings['url'] = settings.get('api_compute', )
        if settings.get('username'):
            settings['identity'] = settings['username']
        if settings.get('password'):
            settings['secret'] = settings['password']
        if settings.get('access_key_id'):
            settings['identity'] = settings['access_key_id']
        if settings.get('secret_key'):
            settings['secret'] = settings['secret_key']
        if settings.get('ca_bundle'):
            settings['verify'] = settings['ca_bundle']
        # Add current settings that may not be present in older settings files.
        if 'name' not in settings:
            settings['name'] = ''
        if 'url' not in settings:
            settings['url'] = ''
        if 'identity' not in settings:
            settings['identity'] = ''
        if 'secret' not in settings:
            settings['secret'] = ''
        if 'verify' not in settings:
            settings['verify'] = ''
        if 'logger' not in settings:
            settings['logger'] = ''
        return settings

    # Write settings.

    def write_settings_file(self, args):
        settings_file_name = self.specified_or_default_settings_file(args.config)
        if not os.path.exists(self.CONFIG_DIRECTORY):
            os.makedirs(self.CONFIG_DIRECTORY)
        if not os.path.exists(self.CONFIG_DIRECTORY):
            self.error_and_exit(400, 'Cannot create the settings directory (%s)' % self.CONFIG_DIRECTORY)
        settings = {}
        settings['name']        = args.name
        settings['url']         = self.normalize_api(args.url)
        settings['identity']    = args.identity
        settings['secret']      = args.secret
        settings['verify']      = args.verify
        settings['logger']      = args.logger
        self.write_json_file(settings_file_name, settings, pretty=True)

    # Output settings.

    @classmethod
    def print_settings(cls, settings):
        print('Settings:')
        print()
        if settings['name'] != '':
            print('Prisma Cloud Tenant (or Compute Console) Name:')
            print(settings['name'])
            print()
        if settings['url'] != '':
            print('Prisma Cloud URL:')
            print(settings['url'])
            print()
        if settings['identity'] != '':
            print('Prisma Cloud Access Key (or Compute Username):')
            print(settings['identity'])
            print()
        if settings['secret'] != '':
            print('Prisma Cloud Secret Key (or Compute Password):')
            print(settings['secret'])
            print()
        if settings['verify'] != '':
            print('SSL Verification:')
            print(settings['verify'])

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
        if '.prismacloud.io' in api:
            api = api.replace('app', 'api')
            api = api.replace('redlock', 'prismacloud')
        api = api.replace('http://', '')
        api = api.replace('https://', '')
        api = api.rstrip('/')
        return api

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
    def error_and_exit(cls, _error_code, error_message=None, system_message=None):
        print()
        print()
        # print('Status Code: %s' % error_code)
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
