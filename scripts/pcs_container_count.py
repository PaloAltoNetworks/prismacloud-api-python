""" Get a Count of Protected Containers """

from pc_lib import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
args = parser.parse_args()

# --Helpers-- #


# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

containers = pc_api.execute_compute('GET', 'api/v1/containers/count')
print(containers)
