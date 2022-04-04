""" Returns a list of repositories that are integrated with Prisma Cloud Code Security """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

print('API - Getting the list of repositories that are integrated with Prisma Cloud Code Security ...', end='')
repositories = pc_api.repositories_list_read(query_params = {'errorsCount': 'true'})
print(' done.')
print()

print('Code Repositories:')

for repository in repositories:
    if repository['source'].lower() == 'cli':
        continue
    print('Code Repository: %s/%s/%s' % (repository['source'].lower(), repository['owner'], repository['repository']))
    print('\tID: %s' % repository['id'])
    if repository['lastScanDate']:
        print('\tLast Scan Date: %s' % repository['lastScanDate'])
        if 'errors' in repository:
            print('\tErrors: %s' % repository['errors'])
    print()
