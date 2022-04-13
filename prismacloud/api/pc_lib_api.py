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
        self.api                = ""
        self.api_compute        = ""
        self.username           = None
        self.password           = None
        self.ca_bundle          = True
        #
        self.token              = None
        self.token_timer        = 0
        self.token_limit        = 540 # aka 9 minutes
        self.retry_limit        = 3
        self.retry_pause        = 8
        self.retry_status_codes = [401, 429, 500, 502, 503, 504]
        self.max_workers        = 8
        #
        self.debug              = False
        self.error_log          = 'error.log'
        self.logger             = None

    def __repr__(self):
        return 'PrismaCloudAPI:\n  API: %s\n  Compute API: %s\n  API Error Count: %s\n  API Token: %s' % (self.api, self.api_compute, self.logger.error.counter, self.token)

    def configure(self, settings):
        # One of API (--api) or API Compute (--api_compute) are required.
        self.api         = settings['api']
        self.api_compute = settings['api_compute']
        self.username    = settings['username']
        self.password    = settings['password']
        self.ca_bundle   = settings['ca_bundle']
        #
        if 'debug' in settings:
            self.debug = settings['debug']
        self.logger = logging.getLogger(__name__)
        formatter   = logging.Formatter(fmt='%(asctime)s: %(levelname)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
        filehandler = logging.FileHandler(self.error_log, delay=True)
        filehandler.setLevel(level=logging.DEBUG)
        filehandler.setFormatter(formatter)
        self.logger.addHandler(filehandler)
        self.logger.error = CallCounter(self.logger.error)
        #
        self.auto_configure_compute()

    def auto_configure_compute(self):
        if self.api and not self.api_compute:
            meta_info = self.meta_info()
            if meta_info and 'twistlockUrl' in meta_info:
                self.api_compute = PrismaCloudUtility.normalize_api_compute(meta_info['twistlockUrl'])
