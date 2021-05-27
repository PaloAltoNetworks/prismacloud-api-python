""" Prisma Cloud API Class """

# Legacy SDK Version 1.0.

from .legacy.config_helper import ConfigHelper
from .legacy.redlock_sdk import RLSession

# SDK Version 2.0.

from .pc_lib_api import PrismaCloudAPI
from .pc_lib_utility import PrismaCloudUtility

__author__  = 'Palo Alto Networks CSE/SE Team'
__version__ = '2.0'

# --Class Instances-- #

pc_api = PrismaCloudAPI()
pc_utility = PrismaCloudUtility()
