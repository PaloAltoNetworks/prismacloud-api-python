""" Prisma Cloud CWP API Class """

import sys

from .compute      import PrismaCloudAPIComputeMixin
from ._containers  import ContainersPrismaCloudAPIComputeMixin
from ._credentials import CredentialsPrismaCloudAPIComputeMixin
from ._images      import ImagesPrismaCloudAPIComputeMixin
from ._registry    import RegistryPrismaCloudAPIComputeMixin
from ._scans       import ScansPrismaCloudAPIComputeMixin
from ._status      import StatusPrismaCloudAPIComputeMixin

mixin_classes_as_strings = list(filter(lambda x: x.endswith('PrismaCloudAPIComputeMixin'), dir()))
mixin_classes = [getattr(sys.modules[__name__], x) for x in mixin_classes_as_strings]

# pylint: disable=too-few-public-methods
class PrismaCloudAPICompute(*mixin_classes):
    """ Prisma Cloud CWP API Class """
