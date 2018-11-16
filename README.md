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
- Use this to set up your Redlock username, password, and customer name for use in the remaining tools.  You add the -u and -p switch with your username and password used to log into the Redlock UI.  The -c switch should be the customer name for your account (this is case sensitive at this time).  Please do not add any ' or " to the keys as it will store the exact thing you type/paste in.
- Also you can run this without any args to see what e-mail and customer is being used.

NOTE: This is stored in clear JSON text in the same folder as the tools.  Keep the resulting conf file protected and do not give it out to anyone.

Example:
```
python rl-configure.py -u user@email.com -p somepasswordhere -c SomeCaseSensitiveCustomerAccountName
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
