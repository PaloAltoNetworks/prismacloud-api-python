
SETTINGS = {
    'name':     'Example Tenant',
    'identity': 'abc',
    'secret':   'def',
    'url':      'example.prismacloud.io',
    'verify':   False,
    'debug':    False
}

META_INFO = {
    'twistlockUrl': 'example.prismacloud.io'
}

USER_PROFILE = {
    'email': 'example@example.com',
    'firstName': 'Example',
    'lastName': 'User',
    'timeZone': 'America/Los_Angeles',
    'enabled': True,
    'lastModifiedBy': 'template@redlock.io',
    'lastModifiedTs': 1630000000000,
    'lastLoginTs': 1640000000000,
    'displayName': 'Example User',
    'accessKeysAllowed': True,
    'defaultRoleId': '1234-5678',
    'roleIds': ['1234-5678'],
    'roles': [{
        'id': '1234-5678',
        'name': 'System Admin',
        'type': 'System Admin',
        'onlyAllowCIAccess': False,
        'onlyAllowComputeAccess': False,
        'onlyAllowReadAccess': False
    }],
    'activeRole': {
        'id': '1234-5678',
        'name': 'System Admin',
        'type': 'System Admin',
        'onlyAllowCIAccess': False,
        'onlyAllowComputeAccess': False,
        'onlyAllowReadAccess': False
    }
}
