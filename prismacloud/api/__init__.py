""" Prisma Cloud API Class """

import sys

from .pc_lib_api import PrismaCloudAPI
from .pc_lib_utility import PrismaCloudUtility
from .version import version as api_version

__author__  = 'Palo Alto Networks CSE/SE/SA Teams'
__version__ = api_version

MIN_PYTHON = (3, 6)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

# --Class Instances-- #

pc_api = PrismaCloudAPI()
pc_utility = PrismaCloudUtility()
