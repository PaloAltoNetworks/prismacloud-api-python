""" Bulk archive compute runtime incidents """

# See workflow in scripts/README.md

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    "input_csv",
    type=str,
    help="Name of input CSV with incidents to archive in the 'ID' field.  This CSV MUST have a header row.",
)
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

# Get incident IDs from CSV
incidents_in = pc_utility.read_csv_file_text(args.input_csv)

# Remove duplicate IDs
incidents_to_archive = {s["ID"] for s in incidents_in}

# Provide a chance to back out
print(f"Preparing to archive {len(incidents_to_archive)} incidents ...")
pc_utility.prompt_for_verification_to_continue(args)

for incident in incidents_to_archive:
    pc_api.audits_ack_incident(incident, ack_status=True)
    print(f"Archived incident {incident}")
