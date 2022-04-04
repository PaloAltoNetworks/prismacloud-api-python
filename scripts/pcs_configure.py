""" Read or write command-line parameters to a configuration file  """

# pylint: disable=import-error
from prismacloud.api import pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
args = parser.parse_args()

# --Main-- #

pc_utility.configure(args)
