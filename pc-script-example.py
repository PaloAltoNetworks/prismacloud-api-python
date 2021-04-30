from pc_lib_api import pc_api
import pc_lib_general

# --Configuration-- #

parser = pc_lib_general.pc_arg_parser_defaults()
args = parser.parse_args()

# --Initialize-- #

pc_api.configure(pc_lib_general.pc_settings_get(args))

# --Main-- #

result = pc_api.current_user()
print(result)