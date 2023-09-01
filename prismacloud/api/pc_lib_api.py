""" Prisma Cloud API Class """

import logging

from .cspm import PrismaCloudAPICSPM
from .cwpp import PrismaCloudAPICWPP
from .pccs import PrismaCloudAPIPCCS

from .pc_lib_utility import PrismaCloudUtility
from .version import version  # Import version from your version.py

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
class PrismaCloudAPI(PrismaCloudAPICSPM, PrismaCloudAPICWPP, PrismaCloudAPIPCCS):
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
        self.timeout            = None # timeout=(16, 300)
        self.token              = None
        self.token_timer        = 0
        self.token_limit        = 590 # aka 9 minutes
        self.retry_status_codes = [425, 429, 500, 502, 503, 504]
        self.retry_waits        = [1, 2, 4, 8, 16, 32]
        self.max_workers        = 8
        #
        self.error_log          = 'error.log'
        self.logger             = None
        # Set User-Agent
        default_user_agent = f"PrismaCloudAPI/{version}"  # Dynamically set default User-Agent
        self.user_agent = default_user_agent

    def __repr__(self):
        return 'Prisma Cloud API:\n  API: (%s)\n  Compute API: (%s)\n  API Error Count: (%s)\n  API Token: (%s)' % (self.api, self.api_compute, self.logger.error.counter, self.token)

    def configure(self, settings, use_meta_info=True):
        self.name        = settings.get('name', '')
        self.identity    = settings.get('identity')
        self.secret      = settings.get('secret')
        self.verify      = settings.get('verify', True)
        self.debug       = settings.get('debug', False)
        self.user_agent  = settings.get('user_agent', self.user_agent)
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
        url = PrismaCloudUtility.normalize_url(settings.get('url', ''))
        if url:
            if url.endswith('.prismacloud.io') or url.endswith('.prismacloud.cn'):
                # URL is a Prisma Cloud CSPM API URL.
                self.api = url
                # Use the Prisma Cloud CSPM API to identify the Prisma Cloud CWP API URL.
                if use_meta_info:
                    meta_info = self.meta_info()
                    if meta_info and 'twistlockUrl' in meta_info:
                        self.api_compute = PrismaCloudUtility.normalize_url(meta_info['twistlockUrl'])
            else:
                # URL is a Prisma Cloud CWP API URL.
                self.api_compute = PrismaCloudUtility.normalize_url(url)

    # Conditional printing.

    def debug_print(self, message):
        if self.debug:
            print(message)
