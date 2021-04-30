from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
from pc_lib_api import pc_api
import pc_lib_general

# --Configuration-- #

parser = pc_lib_general.pc_arg_parser_defaults()
# INSERT SCRIPT-SPECIFIC ARGUMENTS HERE
args = parser.parse_args()

# --Initialize-- #

pc_lib_general.prompt_for_verification_to_continue(args)
pc_settings = pc_lib_general.pc_settings_get(args)
pc_api.configure(pc_settings)

# --Main-- #

# INSERT SCRIPT CODE HERE
result = pc_api.current_user()
print(result)