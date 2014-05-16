import asyncore,time,signal,sys
from secure_smtpd import SMTPServer, FakeCredentialValidator

class SecureSMTPServer(SMTPServer):
    
    def __init__(self):
        pass
        
    def process_message(self, peer, mailfrom, rcpttos, message_data):
        pass
        
    def start(self):
        SMTPServer.__init__(
            self,
            ('0.0.0.0', 25),
            None
        )
        asyncore.loop()
        
server = SecureSMTPServer()
server.start()


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
