from .pc_lib_api import PrismaCloudAPI
from .pc_lib_utility import PrismaCloudUtility

# Backward compatibility with SDK Version 1.0.

from .lib.config_helper import ConfigHelper
from .lib.redlock_sdk import RLSession

__author__  = 'Palo Alto Networks CSE/SE Team'
__version__ = '2.0'

# --Class Instances-- #

pc_api = PrismaCloudAPI()
pc_utility = PrismaCloudUtility()
