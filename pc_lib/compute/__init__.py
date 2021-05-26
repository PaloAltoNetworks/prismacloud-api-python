import sys

from .compute import PrismaCloudAPICompute_Mixin
from ._images import Images_PrismaCloudAPICompute_Mixin
from ._scans  import Scans_PrismaCloudAPICompute_Mixin
from ._status import Status_PrismaCloudAPICompute_Mixin

mixin_classes_as_strings = list(filter(lambda x: x.endswith('PrismaCloudAPICompute_Mixin'), dir()))
mixin_classes = [getattr(sys.modules[__name__], x) for x in mixin_classes_as_strings]

# pylint: disable=too-few-public-methods
class PrismaCloudAPICompute(*mixin_classes):
    pass