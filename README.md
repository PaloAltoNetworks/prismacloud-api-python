# rl-toolbox
Redlock API tools for convenience and general utility.

There are multiple tools that can be used (listed below).  Everything here is written in Python (2.7, specifically - though it may work with Python 3).

If you need to install python, you can get more information at [Python's Page](https://www.python.org/).  I also highly recommend you install the [PIP package manager for Python](https://pypi.python.org/pypi/pip) if you do not already have it installed.

To set up your python environment, you will need the following packages:
- requests

To install/check for this:
```
pip install requests --upgrade
```

------------------------------------------------------------------

On to the tools themselves (Everything requires the rl_api_lib.py library file - keep it in the same directory as the other tools):

**rl-configure.py**
- Use this to set up your Redlock username, password, and customer name for use in the remaining tools.
- REQUIRED - -u switch for the username used to log into the Redlock UI.
- REQUIRED - -p switch for the password used to log into the Redlock UI.
- REQUIRED - -c switch for the customer name (tenant name) for your account (this is case sensitive at this time).
- REQUIRED - -url switch for the Redlock UI base URL found in the URL used to access the Redlock UI (app.redlock.io, app2.redlock.io, etc.)
- Also you can run this without any args to see what e-mail and customer is being used.

NOTE: This is stored in clear JSON text in the same folder as the tools.  Keep the resulting conf file protected and do not give it out to anyone.

Example:
```
python rl-configure.py -u "user@email.com" -p "somepasswordhere" -c "SomeCaseSensitiveCustomerAccountName" -url "app.redlock.io"
```

**rl-policy-status.py**
- Use this to enable/disable policies globally for an account (filtered on policy type).
- It will enable or disable all policies of a given type (or all) for a customer account (global).  This is used primarity for setting up a new environment that wants to begin with everything enabled out of the gate or to update after a large number of new policies have been released.

Example:
```
python rl-policy-status.py config enable
```

**rl-user-import.py**
- Use this to import a list of users from a CSV file.
- It will import the list from CSV then try to check for duplicates before import.

Example:
```
python rl-user-import.py "some user list.csv" "Redlock user role name for my new users"
```

**rl-compliance-copy.py**
- Use this to copy an existing Compliance Standard (and related requirements and sections) into a new Compliance Standard.
- It will copy the entire specified standard into the new standard name specified.  Please use the -policy switch to also attempt to add the newly copied standard to all of the existing standards attached policies.
- If you would like to also add a label to a policy object with the new compliance name, use the -label switch.  This will add a label to any policy attached (must be used witht he -policy switch, otherwise it will be ignored).
- Note: The policy attachment is currently having some issues with updating certain built-in policies.  I am working on this, but at this moment, it will simply skip any policies it has an issue updating and give a list on the command line of the ones it has issues with.  This list can then be manually attached to the new standard after the copy completes.

Example:
```
python rl-compliance-copy.py "SOC 2" "SOC 2 Copy" -policy
```

**rl-compliance-export.py**
- Use this to export an existing Compliance Standard (and related requirements and sections) into a file for import later or in another tenant.

Example:
```
python rl-compliance-export.py "SOC 2" "soc2.json"
```

**rl-compliance-import.py**
- Use this to import a saved Compliance Standard (and related requirements and sections) into a new Compliance Standard in Redlock.
- It will copy the entire specified standard into the new standard name specified.
- Note: This will import the Standard, Requirements, and Sections.  It will NOT attach policies (yet - working on this).

Example:
```
python rl-compliance-import.py "soc2.json" "SOC 2 Copy"
```
