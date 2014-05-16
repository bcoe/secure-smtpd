#!/usr/bin/env python
import asyncore,time,signal,sys
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

    ProxyServer(*args, **kwargs)
    asyncore.loop()

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


# normal termination of this process will kill worker children in
# process pool so this process (the parent) needs to idle here waiting
# for termination signal.  If you don't have a signal handler, then
# Python multiprocess cleanup stuff doesn't happen, and children won't
# get killed by sending SIGTERM to parent.

def sig_handler(signal,frame):
    print "Got signal %s, shutting down." % signal
    sys.exit(0)

signal.signal(signal.SIGTERM, sig_handler)

while 1:
    time.sleep(1)
