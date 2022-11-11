""" Prisma Cloud API Class """

import logging

from .posture import PrismaCloudAPIPosture
from .code_security import PrismaCloudAPICodeSecurity
from .compute import PrismaCloudAPICompute
from .pc_lib_utility import PrismaCloudUtility

# --Description-- #

# Prisma Cloud API library.

# pylint: disable=too-few-public-methods
class CallCounter:
    """ Decorator to determine number of calls for a method """
    def __init__(self, method):
        self.method = method
        self.counter = 0

    def __call__(self, *args, **kwargs):
        self.counter += 1
        return self.method(*args, **kwargs)

# pylint: disable=too-many-instance-attributes
class PrismaCloudAPI(PrismaCloudAPIPosture, PrismaCloudAPICompute, PrismaCloudAPICodeSecurity):
    """ Prisma Cloud API Class """
    # pylint: disable=super-init-not-called
    def __init__(self):
        self.name               = ''
        self.api                = ''
        self.api_compute        = ''
        self.identity           = None
        self.secret             = None
        self.verify             = True
        self.debug              = False
        #
        self.token              = None
        self.token_timer        = 0
        self.token_limit        = 590 # aka 9 minutes
        self.retry_status_codes = [401, 425, 429, 500, 502, 503, 504]
        self.retry_waits        = [1, 2, 4, 8, 16, 32]
        self.max_workers        = 8
        #
        self.error_log          = 'error.log'
        self.logger             = None

    def __repr__(self):
        return 'Prisma Cloud API:\n  API: %s\n  Compute API: %s\n  API Error Count: %s\n  API Token: %s' % (self.api, self.api_compute, self.logger.error.counter, self.token)

    def configure(self, settings):
        self.name        = settings.get('name', '')
        self.api         = settings.get('url', '')
        # See map_cli_config_to_api_config() in https://github.com/PaloAltoNetworks/prismacloud-cli/prismacloud/cli/api.py
        self.api_compute = settings.get('url_compute', '')
        #
        self.identity    = settings['identity']
        self.secret      = settings['secret']
        self.verify      = settings.get('verify', False)
        self.debug       = settings.get('debug', False)
        #
        # self.logger      = settings['logger']
        self.logger = logging.getLogger(__name__)
        formatter   = logging.Formatter(fmt='%(asctime)s: %(levelname)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
        filehandler = logging.FileHandler(self.error_log, delay=True)
        filehandler.setLevel(level=logging.DEBUG)
        filehandler.setFormatter(formatter)
        self.logger.addHandler(filehandler)
        self.logger.error = CallCounter(self.logger.error)
        #
        self.auto_configure_urls()

    # Use the Prisma Cloud CSPM API to identify the Prisma Cloud CWP API URL.

    def auto_configure_urls(self):
        if self.api and not self.api_compute:
            if '.prismacloud.io' in self.api:
                meta_info = self.meta_info()
                if meta_info and 'twistlockUrl' in meta_info:
                    self.api_compute = PrismaCloudUtility.normalize_api(meta_info['twistlockUrl'])
            else:
                self.api_compute = PrismaCloudUtility.normalize_api(self.api)
                self.api = ''

    # Conditional printing.

    def debug_print(self, message):
        if self.debug:
            print(message)
