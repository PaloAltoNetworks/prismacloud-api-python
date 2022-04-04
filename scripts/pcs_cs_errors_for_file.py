""" Returns a list of potential Code Security policy violations for the specified file path """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--filepath',
    required=True,
    type=str,
    help='File')
parser.add_argument(
    '--repository',
    required=True,
    type=str,
    help='Repository name')
parser.add_argument(
    '--sourcetype',
    required=True,
    choices=['Github', 'Bitbucket', 'Gitlab', 'AzureRepos', 'cli', 'AWS', 'Azure', 'GCP', 'Docker', 'githubEnterprise', 'gitlabEnterprise', 'bitbucketEnterprise', 'terraformCloud', 'githubActions', 'circleci', 'codebuild', 'jenkins', 'tfcRunTasks'],
    type=str,
    help='Source')
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

criteria = {
    'filePath':    args.filepath,
    'repository':  args.repository,
    'sourceTypes': args.sourcetype,
    }

print('API - Getting the policy violations for the specified file path ...', end='')
errors = pc_api.errors_file_list(criteria=criteria)
print(' done.')
print()

for error in errors:
    print('File Path: %s' % error['filePath'])
    print('\tID: %s' % error['errorId'])
    print('\tStatus: %s' % error['status'])
    print()

print('Total number of issues/errors/volations: %s' % len(errors))
