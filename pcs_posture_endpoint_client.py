""" Generic Prisma Cloud API Endpoint Client. """

from json import dumps as json_dumps
from os import isatty
from pc_lib import pc_api, pc_utility
from sys import stderr, stdout

# --Configuration-- #

parser = pc_utility.get_arg_parser()

parser.add_argument(
    'http_method',
    type=str,
    help='HTTP Method for HTTP request')

parser.add_argument(
    'uri_path',
    type=str,
    help='URI Path to HTTP endpoint')

parser.add_argument(
    '--uri_params',
    type=str,
    help='(Optional) URI Parameters for HTTP request')

parser.add_argument(
    '--import_file_name',
    type=str,
    help='(Optional) Import file name for file containing the HTTP request body data.')

args = parser.parse_args()

if not args.uri_params:
  args.uri_params = ''

if not args.import_file_name:
  args.import_file_name = ''

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

if args.import_file_name == '':
    import_file_data = None
    if args.uri_params == '':
        print('API - Executing HTTP request "%s %s"' % (args.http_method, args.uri_path), file=stderr)
    else:
        print('API - Executing HTTP request "%s %s&%s"' % (args.http_method, args.uri_path, args.uri_params), file=stderr)
else:
    # Import the data file
    print('API - Importing file data from file %s' % args.import_file_name, file=stderr)
    try:
        import_file_data = pc_utility.read_json_file(args.import_file_name)
        print('API - Import of file data %s completed' % args.import_file_name, file=stderr)
        if args.uri_params == '':
            print('API - Executing HTTP request "%s %s" with request body:\n%s' % (args.http_method, args.uri_path, import_file_data), file=stderr) 
        else:
            print('API - Executing HTTP request "%s %s&%s" with request body:\n%s' %  (args.http_method, args.uri_path, args.uri_params, import_file_data), file=stderr)
    except:
        print('API - Failed to import file %s' % args.import_file_name, file=stderr)
        exit(1)

# HUGE WARNING: NO VALIDATION HERE IN THIS EXAMPLE (so that it fits the broadest set of use-cases)

# Prompt for warning if interactive
if isatty(stdout.fileno()):
  pc_utility.prompt_for_verification_to_continue(args)

# Make the HTTP request

try:
    response=pc_api.execute(args.http_method,args.uri_path,query_params=args.uri_params,body_params=import_file_data)
    print('API - HTTP request response is:', file=stderr)
    print(json_dumps(response), file=stdout)
except:
    print('API - HTTP request failed', file=stderr)
    exit(2)


