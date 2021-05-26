import logging

from .posture import PrismaCloudAPIPosture
from .compute import PrismaCloudAPICompute

# --Description-- #

# Prisma Cloud API library.

# --Class Methods-- #

# pylint: disable=too-few-public-methods
class CallCounter:
    # Decorator to determine number of calls for a method.
    def __init__(self, method):
        self.method = method
        self.counter = 0

    def __call__(self, *args, **kwargs):
        self.counter += 1
        return self.method(*args, **kwargs)

# pylint: disable=too-many-instance-attributes
class PrismaCloudAPI(PrismaCloudAPIPosture, PrismaCloudAPICompute):
    # pylint: disable=super-init-not-called
    def __init__(self):
        self.api                = None
        self.api_compute        = None
        self.username           = None
        self.password           = None
        self.ca_bundle          = None
        self.token              = None
        self.token_timer        = 0
        self.token_limit        = 540
        self.retry_limit        = 3
        self.retry_pause        = 5
        self.retry_status_codes = [401, 429, 500, 502, 503, 504]
        self.max_workers        = 16
        self.error_log          = 'error.log'
        self.logger             = None

    def __repr__(self):
        return 'PrismaCloudAPI:\n  API: %s\n  Compute API: %s\n  API Error Count: %s\n  API Token: %s' % (self.api, self.api_compute, self.logger.error.counter, self.token)

    def configure(self, settings):
        # Required.
        self.api         = settings['apiBase']
        self.username    = settings['username']
        self.password    = settings['password']
        # Optional.
        self.api_compute = settings['api_compute']
        self.ca_bundle   = settings['ca_bundle']
        # Logging!
        self.logger = logging.getLogger(__name__)
        formatter   = logging.Formatter(fmt='%(asctime)s: %(levelname)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
        filehandler = logging.FileHandler(self.error_log)
        filehandler.setLevel(level=logging.DEBUG)
        filehandler.setFormatter(formatter)
        self.logger.addHandler(filehandler)
        self.logger.error = CallCounter(self.logger.error)
