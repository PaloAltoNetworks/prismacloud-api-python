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
    '--request_body',
    type=str,
    help='(Optional) Import file name for file containing the HTTP request body data.')

parser.add_argument(
    '--response_file',
    type=str,
    help='(Optional) Export file name for file containing the HTTP response body data.')

parser.add_argument(
    '--pretty',
    action='store_true',
    help='(Optional) Specify pretty JSON output.')

args = parser.parse_args()

if not args.uri_params:
  args.uri_params = None

if not args.request_body:
  args.request_body = None

if not args.pretty:
  args.pretty = False

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

if args.request_body == None:
    request_body_data = None
    if args.uri_params == None:
        print('API - Executing HTTP request "%s %s"' % (args.http_method, args.uri_path), file=stderr)
    else:
        print('API - Executing HTTP request "%s %s&%s"' % (args.http_method, args.uri_path, args.uri_params), file=stderr)
else:
    # Import the data file
    print('API - Importing file data from file %s' % args.request_body, file=stderr)
    try:
        request_body_data = pc_utility.read_json_file(args.request_body)
        print('API - Import of file data %s completed' % args.request_body, file=stderr)
        if args.uri_params == '':
            print('API - Executing HTTP request "%s %s" with request body:\n%s' % (args.http_method, args.uri_path, request_body_data), file=stderr) 
        else:
            print('API - Executing HTTP request "%s %s&%s" with request body:\n%s' %  (args.http_method, args.uri_path, args.uri_params, request_body_data), file=stderr)
    except:
        print('API - Failed to import file %s' % args.request_body, file=stderr)
        exit(2)

# HUGE WARNING: NO VALIDATION HERE IN THIS EXAMPLE (so that it fits the broadest set of use-cases)

# Prompt for warning if interactive
if isatty(stdout.fileno()):
  pc_utility.prompt_for_verification_to_continue(args)

# Make the HTTP request

try:
    response=pc_api.execute(args.http_method,args.uri_path,query_params=args.uri_params,body_params=request_body_data)
    if args.response_file == None:
      print('API - HTTP request response is:', file=stderr)
      if args.pretty:
          print(json_dumps(response, indent=4, separators=(', ', ': ')), file=stdout)
      else:
          print(json_dumps(response), file=stdout)
    else:
      print('API - HTTP request response stored in file %s' % args.response_file, file=stderr)
      pc_utility.write_json_file(args.response_file, response, pretty=bool(args.pretty))
except:
    print('API - HTTP request failed', file=stderr)
    exit(1)


