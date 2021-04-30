from OpenSSL import crypto, SSL
import argparse
import certifi
import socket

# --Description-- #

# Prisma Cloud SSL Helper (requires 'pip install certifi pyopenssl')

# --Configuration-- #

pc_arg_parser = argparse.ArgumentParser()
pc_arg_parser.add_argument(
        '--uiurl',
        default='api.prismacloud.io',
        type=str,
        help='(Optional) - Prisma Cloud API/UI Base URL')
pc_arg_parser.add_argument(
        '--ca_bundle',
        default='globalprotect_certifi.txt',
        type=str,
        help='(Optional) - Custom CA (bundle) file to create')
args = pc_arg_parser.parse_args()

src_ca_file = certifi.where()
dst_ca_file = args.ca_bundle
host_name = args.uiurl 
port = 443
panw_subjects = [
    '/C=US/ST=CA/O=paloalto networks/OU=IT/CN=decrypt.paloaltonetworks.com',
    '/DC=local/DC=paloaltonetworks/CN=Palo Alto Networks Inc Domain CA',
    '/C=US/O=Palo Alto Networks Inc/CN=Palo Alto Networks Inc Root CA'
]
ssl_context_method = SSL.TLSv1_2_METHOD # SSL.SSLv23_METHOD

# --Main-- #

src_file = open(src_ca_file, 'r')
root_certificates = src_file.read()
src_file.close()

dst_file = open(dst_ca_file, 'w')
dst_file.write(root_certificates)
        
context = SSL.Context(method=ssl_context_method)
context.load_verify_locations(cafile=src_ca_file)
conn = SSL.Connection(context, socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
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
        certificate_string = crypto.dump_certificate(crypto.FILETYPE_PEM, certificate).decode('utf-8')
        dst_file.write("\n")
        dst_file.write(subject_string)
        dst_file.write("\n")
        dst_file.write(issuer_string)
        dst_file.write("\n")
        dst_file.write(certificate_string)
conn.close()

dst_file.close()

print('Custom CA (bundle) file saved as: %s' % dst_ca_file)
print("Use it with these scripts by specifying '--ca_bundle %s'" % dst_ca_file)