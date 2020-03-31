# pc-toolbox
Prisma Cloud API tools for convenience and general utility.

There are multiple tools that can be used (listed below).  Everything here is written in Python (2.7, origionally, now updated and tested in Python 3.7, but both should still work).

If you need to install python, you can get more information at [Python's Page](https://www.python.org/).  I also highly recommend you install the [PIP package manager for Python](https://pypi.python.org/pypi/pip) if you do not already have it installed.

To set up your python environment, you will need the following packages:
- requests

To install/check for this:
```
pip install requests --upgrade
```

------------------------------------------------------------------

On to the tools themselves (Everything requires the rl_api_lib.py and rl_lib_general.py library files - keep them in the same directory as the other tools):

**pc-configure.py**
- Use this to set up your Prisma Cloud username, password, and URL for use in the remaining tools.
- REQUIRED - -u switch for the Access Key ID generated from your Prisma Cloud user.
- REQUIRED - -p switch for the Secred Key generated from your Prisma Cloud user.
- REQUIRED - -url switch for the Prisma Cloud UI base URL found in the URL used to access the Prisma Cloud UI (app.prismacloud.io, app2.prismacloud.io, etc.).  This will try to translate from the older redlock.io addresses.  You can also put in the direct api.* link as well.
- Also you can run this without any args to see what Access Key ID and URL is being used.

NOTE: This is stored in clear JSON text in the same folder as the tools.  Keep the resulting conf file protected and do not give it out to anyone.

Example:
```
python pc-configure.py -u "accesskeyidhere" -p "secretkeyhere" -url "app3.prismacloud.io"
```

**pc-policy-status.py**
- Use this to enable/disable policies globally for an account (filtered on policy type).
- It will enable or disable all policies of a given type (or all) for a customer account (global).  This is used primarity for setting up a new environment that wants to begin with everything enabled out of the gate or to update after a large number of new policies have been released.

Example:
```
python pc-policy-status.py config enable
```

**pc-user-import.py**
- Use this to import a list of users from a CSV file.
- It will import the list from CSV then try to check for duplicates before import.

Example:
```
python pc-user-import.py "some user list.csv" "Prisma Cloud user role name for my new users"
```

**pc-compliance-copy.py**
- Use this to copy an existing Compliance Standard (and related requirements and sections) into a new Compliance Standard.
- It will copy the entire specified standard into the new standard name specified.  Please use the -policy switch to also attempt to add the newly copied standard to all of the existing standards attached policies.
- If you would like to also add a label to a policy object with the new compliance name, use the -label switch.  This will add a label to any policy attached (must be used witht he -policy switch, otherwise it will be ignored).
- Note: The policy attachment is currently having some issues with updating certain built-in policies.  It will simply skip any policies it has an issue updating and give a list on the command line of the ones it has issues with.  This list can then be manually attached to the new standard after the copy completes.

Example:
```
python pc-compliance-copy.py "SOC 2" "SOC 2 Copy" -policy
```

**pc-compliance-export.py**
- Use this to export an existing Compliance Standard (and related requirements and sections) into a file for import later or in another tenant.

Example:
```
python pc-compliance-export.py "SOC 2" "soc2.json"
```

**pc-compliance-import.py**
- Use this to import a saved Compliance Standard (and related requirements and sections) into a new Compliance Standard in Prisma Cloud.
- It will copy the entire specified standard into the new standard name specified.
- Note: This will import the Standard, Requirements, and Sections.  It will NOT attach policies (yet - working on this).

Example:
```
python pc-compliance-import.py "soc2.json" "SOC 2 Copy"
```

**pc-cloud-account-import-azure.py (in progress)**
- This is the framework for importing a CSV (template in the templates folder) with a list of Azure accounts into Prisma Cloud.
- Note: This is still a work in progress.  Basic import framework is running, but validation of CSV and duplicate name checking has not been implemented yet.

Example:
```
python pc-cloud-account-import-azure.py prisma_cloud_account_import_azure_template.csv
```
