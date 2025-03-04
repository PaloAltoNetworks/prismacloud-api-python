""" Prisma Cloud API Class """

import logging

import requests
from requests.adapters import HTTPAdapter, Retry

from .cspm import PrismaCloudAPICSPM
from .cwpp import PrismaCloudAPICWPP
from .pccs import PrismaCloudAPIPCCS

from .pc_lib_utility import PrismaCloudUtility

import importlib.metadata
version = importlib.metadata.version("prismacloudapi")



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
        self.tenant_id          = None
        self.token              = None
        self.token_timer        = 0
        self.token_limit        = 590 # aka 9 minutes
        self.token_compute      = None
        self.token_compute_timer= 0
        self.retry_status_codes = [425, 429, 500, 502, 503, 504]
        self.retry_waits        = [1, 2, 4, 8, 16, 32]
        self.retry_allowed_methods = frozenset(["GET", "POST"])
        self.max_workers        = 8
        #
        self.error_log          = 'error.log'
        self.logger             = None
        # Set User-Agent
        self.user_agent = f"PrismaCloudAPI/{version}"  # Dynamically set default User-Agent
        # use a session
        self.session = requests.session()
        self.session_compute = requests.session()
        retries = Retry(total=6, status=6, backoff_factor=1, status_forcelist=self.retry_status_codes,
                        allowed_methods=self.retry_allowed_methods)
        self.session_adapter = HTTPAdapter(max_retries=retries)
        # CSPM
        self.session.headers['User-Agent'] = self.user_agent
        self.session.headers['Content-Type'] = 'application/json'
        # CWP
        self.session_compute.headers['User-Agent'] = self.user_agent
        self.session_compute.headers['Content-Type'] = 'application/json'

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
                self.session.mount(f"https://{url}", self.session_adapter)
                self.debug_print(f"Mounted retry adapter on API {url}")
                # Use the Prisma Cloud CSPM API to identify the Prisma Cloud CWP API URL.
                if use_meta_info:
                    meta_info = self.meta_info()
                    if meta_info and 'twistlockUrl' in meta_info:
                        self.api_compute = PrismaCloudUtility.normalize_url(meta_info['twistlockUrl'])
                        self.session.mount(f"https://{self.api_compute}", self.session_adapter)
                        self.debug_print(f"Mounted retry adapter on API Compute {self.api_compute}")
            else:
                # URL is a Prisma Cloud CWP API URL.
                self.api_compute = PrismaCloudUtility.normalize_url(url)
                self.session.mount(f"https://{self.api_compute}", self.session_adapter)
                self.debug_print(f"Mounted retry adapter on API Compute {self.api_compute}")
        if not self.api and not self.api_compute:
            self.error_and_exit(418, "Specify a Prisma Cloud URL or Prisma Cloud Compute URL")

    # Conditional printing.

    def debug_print(self, message):
        if self.debug:
            logging.debug(message)
