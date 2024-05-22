""" Prisma Cloud CWP API Class """

import sys

from .cwpp import *
from ._audits import *
from ._cloud import *
from ._collections import *
from ._containers import *
from ._credentials import *
from ._defenders import *
from ._feeds import *
from ._hosts import *
from ._images import *
from ._logs import *
from ._policies import *
from ._registry import *
from ._scans import *
from ._settings import *
from ._serverless import *
from ._stats import *
from ._status import *
from ._tags import *
from ._vms import *

mixin_classes_as_strings = list(
    filter(lambda x: x.endswith('PrismaCloudAPICWPPMixin'), dir()))
mixin_classes = [getattr(sys.modules[__name__], x)
                 for x in mixin_classes_as_strings]

# pylint: disable=too-few-public-methods


class PrismaCloudAPICWPP(*mixin_classes):
    """ Prisma Cloud CWP API Class """
