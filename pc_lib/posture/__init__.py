""" Prisma Cloud CSPM API Class """

import sys

from .posture import PrismaCloudAPIMixin
from ._endpoints import EndpointsPrismaCloudAPIMixin
from ._extended import ExtendedPrismaCloudAPIMixin

mixin_classes_as_strings = list(filter(lambda x: x.endswith('PrismaCloudAPIMixin'), dir()))
mixin_classes = [getattr(sys.modules[__name__], x) for x in mixin_classes_as_strings]

# pylint: disable=too-few-public-methods
class PrismaCloudAPIPosture(*mixin_classes):
    """ Prisma Cloud CSPM API Class """
