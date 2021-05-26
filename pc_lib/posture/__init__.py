import sys

from .posture import PrismaCloudAPI_Mixin
from ._endpoints import Endpoints_PrismaCloudAPI_Mixin
from ._extended import Extended_PrismaCloudAPI_Mixin

mixin_classes_as_strings = list(filter(lambda x: x.endswith('PrismaCloudAPI_Mixin'), dir()))
mixin_classes = [getattr(sys.modules[__name__], x) for x in mixin_classes_as_strings]

# pylint: disable=too-few-public-methods
class PrismaCloudAPIPosture(*mixin_classes):
    pass
