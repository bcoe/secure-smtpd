#!/usr/bin/env python
import argparse
from secure_smtpd import ProxyServer

def run(cmdargs):
    args = [
        (cmdargs.localhost, cmdargs.localport),
        (cmdargs.remotehost, cmdargs.remoteport)
    ]
    kwargs = {}

    if cmdargs.sslboth:
        kwargs['ssl'] = True
    elif cmdargs.sslout:
        kwargs['ssl_out_only'] = True

    if not cmdargs.quiet:
        kwargs['debug'] = True

    server = ProxyServer(*args, **kwargs)
    server.run()

parser = argparse.ArgumentParser(description='mail relay tool')

parser.add_argument(
    '--localhost',
    default='127.0.0.1',
    help='Local address to attach to for receiving mail.  Defaults to 127.0.0.1'
)
    
parser.add_argument(
    '--localport',
    default=1025,
    type=int,
    help='Local port to attach to for receiving mail.  Defaults to 1025'
)

parser.add_argument(
    '--remotehost',
    required=True,
    help='Address of the remote server for connection.'
)

parser.add_argument(
    '--remoteport',
    default=25,
    type=int, 
    help='Port of the remote server for connection.  Defaults to 25'
)

parser.add_argument(
    '--quiet',
    action='store_true',
    help='Use this to turn off the message printing'
)

group = parser.add_mutually_exclusive_group()

group.add_argument(
    '--sslboth',
    action='store_true', 
    help='Use this parameter if both the inbound and outbound connections should use SSL'
)
    
group.add_argument(
    '--sslout',
    action='store_true', 
    help='Use this parameter if inbound connection is plain but the outbound connection uses SSL'
)

args = parser.parse_args()

print 'Starting ProxyServer'
print 'local: %s:%s' % (args.localhost, args.localport)
print 'remote: %s:%s' % (args.remotehost, args.remoteport)
print 'sslboth: ', args.sslboth
print 'sslout: ', args.sslout
print
run(args)
