""" Prisma Cloud API Class """

import sys

from prismacloud.pc_lib_api import PrismaCloudAPI
from prismacloud.pc_lib_utility import PrismaCloudUtility

MIN_PYTHON = (3, 6)
if sys.version_info < MIN_PYTHON:
    raise SystemExit("Python %s.%s or later is required.\n" % MIN_PYTHON)

# --Class Instances-- #

pc_api = PrismaCloudAPI()
pc_utility = PrismaCloudUtility()
