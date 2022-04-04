""" Prisma Cloud Code Security API Class """

import sys

from .code_security import *
from ._errors       import *
from ._fixes        import *
from ._repositories import *
from ._scans        import *
from ._suppressions import *

mixin_classes_as_strings = list(filter(lambda x: x.endswith('PrismaCloudAPICodeSecurityMixin'), dir()))
mixin_classes = [getattr(sys.modules[__name__], x) for x in mixin_classes_as_strings]

# pylint: disable=too-few-public-methods
class PrismaCloudAPICodeSecurity(*mixin_classes):
    """ Prisma Cloud Code Security API Class """
