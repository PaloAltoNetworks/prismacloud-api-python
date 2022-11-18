# Python SDK for the Prisma Cloud APIs

This project includes a Python SDK for the Prisma Cloud APIs (CSPM, CWPP, and PCCS) in the form of a Python package.
It also includes reference scripts that utilize the SDK.

Major changes with Version 5.0:

* Command-line argument and configuration file changes.

## Table of Contents

* [Setup](#Setup)
* [Support](#Support)


## Setup

Install the SDK via:

```
pip3 install prismacloud-api
```

### Reference Scripts

Please refer to the example/reference [scripts](https://github.com/PaloAltoNetworks/prismacloud-api-python/tree/main/scripts) directory for documentation and usage details.

If you prefer to use the SDK without using command line options, consider this minimal example:

```
import os
from prismacloud.api import pc_api

sass_settings = {
    "url":      "api.prismacloud.io",
    "identity": "accesskey",
    "secret":   "secretkey"
}

on_premise_settings = {
    "url":      "console.example.com",
    "identity": "username",
    "secret":   "password"
}

env_settings = {
    "url":      os.environ.get('PC_URL'),
    "identity": os.environ.get('PC_IDENTITY'),
    "secret":   os.environ.get('PC_SECRET')
}

pc_api.configure(sass_settings)

if pc_api.api:
    print()
    print('Prisma Cloud API Test:')
    print()
    print(pc_api.current_user())

if pc_api.api_compute:
    print()
    print('Prisma Cloud Compute API Test:')
    print()
    print(pc_api.statuses_intelligence())
    print()
```

## Support

This project has been developed by Prisma Cloud SEs, it is not Supported by Palo Alto Networks.
Nevertheless, the maintainers will make a best-effort to address issues, and (of course) contributors are encouraged to submit issues and pull requests.
