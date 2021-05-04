from .pc_lib_api import PrismaCloudAPI
from .pc_lib_utility import PrismaCloudUtility

# Backward compatibility with SDK Version 1.0.

from .redlock_sdk import RLSession
from .config_helper import ConfigHelper

__author__  = 'Palo Alto Networks CSE/SE Team'
__version__ = '2.0'

# --Class Instances-- #

pc_api = PrismaCloudAPI()
pc_utility = PrismaCloudUtility()
