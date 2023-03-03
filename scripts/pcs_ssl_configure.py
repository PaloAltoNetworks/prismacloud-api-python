""" Utility to create a certificate bundle including intercepting proxy certificates """

import argparse
import socket
import ssl
import sys
import OpenSSL

import certifi

# --Description-- #

# Utility to create a certificate bundle including intercepting proxy certificates (requires 'pip install certifi pyopenssl')
# Defaults to include certificates used by Global Protect.

# --Configuration-- #

pc_arg_parser = argparse.ArgumentParser()
pc_arg_parser.add_argument(
        '--api',
        default='api.prismacloud.io',
        type=str,
        help='(Optional) - URL')
pc_arg_parser.add_argument(
        '--api_port',
        default=443,
        type=int,
        help='(Optional) - Port.')
pc_arg_parser.add_argument(
        '--ca_bundle',
        default='globalprotect_certifi.txt',
        type=str,
        help='(Optional) - Certificate bundle filename to create')
pc_arg_parser.add_argument(
        '-s',
        dest='custom_subjects',
        default=[
            '/C=US/ST=CA/O=paloalto networks/OU=IT/CN=decrypt.paloaltonetworks.com',
            '/DC=local/DC=paloaltonetworks/CN=Palo Alto Networks Inc Domain CA',
            '/C=US/O=Palo Alto Networks Inc/CN=Palo Alto Networks Inc Root CA'
        ],
        nargs='*',
        type=str,
        help='(Optional) - List of certificate subjects (or substrings) to match')
pc_arg_parser.add_argument(
        '-i', '--insensitive',
        action='store_true',
        help='(Default: disabled) - Enable case-insensitive substring matching')
args = pc_arg_parser.parse_args()

src_ca_file        = certifi.where()
dst_ca_file        = args.ca_bundle
host_name          = args.api
port               = args.api_port
custom_subjects    = args.custom_subjects
ssl_context_method = OpenSSL.SSL.TLSv1_2_METHOD # SSL.SSLv23_METHOD

if args.insensitive:
    custom_subjects = [cs.lower() for cs in custom_subjects]

# --Main-- #

print('Connecting to %s:%s' % (host_name, port))
print('Searching the peer certificate chain for certificates with subjects matching:')
print()
for cs in custom_subjects:
    print('    %s' % cs)
print()
if args.insensitive:
    print('Using case-insensitive substring matching')
print()

with open(src_ca_file, 'r') as root_ca_file:
    root_certificates = root_ca_file.read()

with open(dst_ca_file, 'w') as custom_ca_file:
    custom_ca_file.write(root_certificates)
    context = OpenSSL.SSL.Context(method=ssl_context_method)

    if ssl.OPENSSL_VERSION.startswith('OpenSSL 3'):
        # https://github.com/python/cpython/issues/89051 ("ssl.OP_LEGACY_SERVER_CONNECT missing")
        # context.set_options(OP_LEGACY_SERVER_CONNECT)
        context.set_options(0x4)

    context.load_verify_locations(cafile=src_ca_file)
    conn = OpenSSL.SSL.Connection(context, socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    conn.settimeout(5)
    conn.connect((host_name, port))
    conn.setblocking(1)

    try:
        conn.do_handshake()
    except: # pylint: disable=bare-except
        print()
        print('OpenSSL Error: Unsafe Legacy Renegotiation Disabled')
        print('To resolve, create an openssl.conf file containing the following content ...')
        print()
        print("openssl_conf = openssl_init\n[openssl_init]\nssl_conf = ssl_sect\n\n[ssl_sect]\nsystem_default = system_default_sect\n\n[system_default_sect]\nOptions = UnsafeLegacyRenegotiation")
        print()
        print('... then rerun this script using that file:')
        print('OPENSSL_CONF=./openssl.conf python3 pcs_ssl_configure.py')
        print()
        sys.exit(1)

    found_subjects = []

    conn.set_tlsext_host_name(host_name.encode())
    for (idx, certificate) in enumerate(conn.get_peer_cert_chain()):
        certificate_subject = ''.join("/{0:s}={1:s}".format(name.decode(), value.decode()) for name, value in certificate.get_subject().get_components())
        certificate_issuer  = ''.join("/{0:s}={1:s}".format(name.decode(), value.decode()) for name, value in certificate.get_issuer().get_components())

        if args.insensitive:
            subject_to_match = certificate_subject.lower()
        else:
            subject_to_match = certificate_subject
        certificate_subject_matches = any(custom_subject in subject_to_match for custom_subject in custom_subjects)

        if certificate_subject_matches:
            certificate_subject_comment = '# Subject: %s' % certificate_subject
            certificate_issuer_comment  = '# Issuer: %s' % certificate_issuer
            certificate_string = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate).decode('utf-8')
            custom_ca_file.write("\n")
            custom_ca_file.write(certificate_subject_comment)
            custom_ca_file.write("\n")
            custom_ca_file.write(certificate_issuer_comment)
            custom_ca_file.write("\n")
            custom_ca_file.write(certificate_string)
            found_subjects.append(certificate_subject)
            print('Found matching certificate: %s' % certificate_subject)

    conn.close()

print()
print('Certificate bundle saved as: %s' % dst_ca_file)
