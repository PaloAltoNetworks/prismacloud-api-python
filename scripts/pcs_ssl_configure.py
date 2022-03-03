""" Utility to create a CA bundle including GlobalProtect certificates """

import argparse
import socket
import OpenSSL

import certifi

# --Description-- #

# Prisma Cloud SSL Helper (requires 'pip install certifi pyopenssl')

# --Configuration-- #

pc_arg_parser = argparse.ArgumentParser()
pc_arg_parser.add_argument(
        '--api',
        default='api.prismacloud.io',
        type=str,
        help='(Optional) - Prisma Cloud API/UI Base URL')
pc_arg_parser.add_argument(
        '--api_port',
        default=443,
        type=int,
        help='(Optional) - Prisma Cloud API/UI Port.')
pc_arg_parser.add_argument(
        '--ca_bundle',
        default='globalprotect_certifi.txt',
        type=str,
        help='(Optional) - Custom CA (bundle) file to create')
args = pc_arg_parser.parse_args()

src_ca_file = certifi.where()
dst_ca_file = args.ca_bundle
host_name = args.api
port = args.api_port
panw_subjects = [
    '/C=US/ST=CA/O=paloalto networks/OU=IT/CN=decrypt.paloaltonetworks.com',
    '/DC=local/DC=paloaltonetworks/CN=Palo Alto Networks Inc Domain CA',
    '/C=US/O=Palo Alto Networks Inc/CN=Palo Alto Networks Inc Root CA'
]
ssl_context_method = OpenSSL.SSL.TLSv1_2_METHOD # SSL.SSLv23_METHOD

# --Main-- #

with open(src_ca_file, 'r') as root_ca_file:
    root_certificates = root_ca_file.read()

with open(dst_ca_file, 'w') as custom_ca_file:
    custom_ca_file.write(root_certificates)
    context = OpenSSL.SSL.Context(method=ssl_context_method)
    context.load_verify_locations(cafile=src_ca_file)
    conn = OpenSSL.SSL.Connection(context, socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    conn.settimeout(5)
    conn.connect((host_name, port))
    conn.setblocking(1)
    conn.do_handshake()
    conn.set_tlsext_host_name(host_name.encode())
    for (idx, certificate) in enumerate(conn.get_peer_cert_chain()):
        subject = ''.join("/{0:s}={1:s}".format(name.decode(), value.decode()) for name, value in certificate.get_subject().get_components())
        issuer  = ''.join("/{0:s}={1:s}".format(name.decode(), value.decode()) for name, value in certificate.get_issuer().get_components())
        if subject in panw_subjects:
            subject_string     = '# Subject: %s' % subject
            issuer_string      = '# Issuer: %s' % issuer
            certificate_string = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate).decode('utf-8')
            custom_ca_file.write("\n")
            custom_ca_file.write(subject_string)
            custom_ca_file.write("\n")
            custom_ca_file.write(issuer_string)
            custom_ca_file.write("\n")
            custom_ca_file.write(certificate_string)
    conn.close()

print('Custom CA (bundle) file saved as: %s' % dst_ca_file)
print("Use it with these scripts by specifying '--ca_bundle %s' on the command line or in your config file" % dst_ca_file)
