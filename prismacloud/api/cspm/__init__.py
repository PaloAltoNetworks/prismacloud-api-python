""" Prisma Cloud CSPM API Class """

import sys

from .cspm       import *
from ._endpoints import *
from ._extended  import *

mixin_classes_as_strings = list(filter(lambda x: x.endswith('PrismaCloudAPIMixin'), dir()))
mixin_classes = [getattr(sys.modules[__name__], x) for x in mixin_classes_as_strings]

# pylint: disable=too-few-public-methods
class PrismaCloudAPICSPM(*mixin_classes):
    """ Prisma Cloud CSPM API Class """
