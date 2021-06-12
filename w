A generic API endpoint client for use with Posture API that is suitable for command-line and pipeline use.

All info/debug output is emitted to stderr. Request output is emitted to stdout

Usage:

  ./pcs_posture_endpoint_client.py GET /check 
  ./pcs_posture_endpoint_client.py GET /some_fake_endpoint --uri_params 'debug=true' --import_file_name 'blah.json'

It's very rudimentary but will allow ad-hoc mock-ups of any transaction.


