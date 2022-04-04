""" Add discovered registries to Vulnerability->Images->Registry settings """

from operator import itemgetter

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    "--collection",
    type=str,
    default="All",
    help="(Optional) - Collection to use for scanning, defaults to All.",
)
parser.add_argument(
    "--serviceType",
    type=str,
    choices=["aws-ecr", "azure-acr", "all"],
    default="all",
    help="(Optional) - Add all or specific registry types.",
)
parser.add_argument("--dryrun", action="store_true", help="Set flag for dryrun mode")
args = parser.parse_args()

# --Helpers-- #

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)
pc_api.validate_api_compute()

# --Main-- #

print("API   - Getting all cloud discovered assets ...", end="")
discovered_cloud_assets = pc_api.cloud_discovery_read()
print(" Success.")

print("INFO  - Filtering all discovered registries ...", end="")
discovered_cloud_registries = [
    item for item in discovered_cloud_assets if "registry" in item
]
print(" Success.")
print("INFO  - Discovered registries ... %s" % len(discovered_cloud_registries))
print("API   - Getting all configured registries ...", end="")
configured_registries = pc_api.settings_registry_read()
print(" Success.")
configured_registries_list = list(
    map(itemgetter("registry"), configured_registries["specifications"])
)
print("INFO  - Configured registries ... %s" % len(configured_registries_list))
update = 0
for d_registry in discovered_cloud_registries:
    if (
        args.serviceType in (d_registry["serviceType"], "all")
    ) and (d_registry["registry"] not in configured_registries_list):
        print(
            "INFO  - Adding %s to registry scan queue ..." % d_registry["registry"],
            end="",
        )
        configured_registries["specifications"].append(
            {
                "collections": [args.collection],
                "cap": 5,
                "os": "linux",
                "scanners": 2,
                "registry": d_registry["registry"],
                "version": d_registry["provider"],
                "credentialId": d_registry["credentialId"],
            }
        )
        print(" Success.")
        update = 1
if update:
    if args.dryrun:
        print("DRYRN - Pushing new list of configured registries ... Success.")
    else:
        print("API   - Pushing new list of configured registries ...", end="")
        pc_api.settings_registry_write(
            {"specifications": configured_registries["specifications"]}
        )
        print(" Success.")
else:
    print("INFO  - No registries to add.")
