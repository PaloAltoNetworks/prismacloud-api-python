""" Prisma Cloud API Class """

import sys

from .pc_lib_api import PrismaCloudAPI
from .pc_lib_utility import PrismaCloudUtility

__author__  = 'Palo Alto Networks CSE/SE/SA Teams'
__version__ = '3.0'

MIN_PYTHON = (3, 6)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

# --Class Instances-- #

pc_api = PrismaCloudAPI()
pc_utility = PrismaCloudUtility()
