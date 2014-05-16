import secure_smtpd
import asyncore, logging, time, signal, sys
from secure_smtpd import SMTPServer, FakeCredentialValidator

class SSLSMTPServer(SMTPServer):
    
    def __init__(self):
        pass
        
    def process_message(self, peer, mailfrom, rcpttos, message_data):
        print message_data
        
    def start(self):
        SMTPServer.__init__(
            self,
            ('0.0.0.0', 465),
            None,
            require_authentication=True,
            ssl=True,
            certfile='examples/server.crt',
            keyfile='examples/server.key',
            credential_validator=FakeCredentialValidator(),
            maximum_execution_time = 1.0
        )
        asyncore.loop()

logger = logging.getLogger( secure_smtpd.LOG_NAME )
logger.setLevel(logging.INFO)
server = SSLSMTPServer()
server.start()

# normal termination of this process will kill worker children in
# process pool so this process (the parent) needs to idle here waiting
# for termination signal.  If you don't have a signal handler, then
# Python multiprocess cleanup stuff doesn't happen, and children won't
# get killed by sending SIGTERM to parent.

def sig_handler(signal,frame):
    logger.info("Got signal %s, shutting down." % signal)
    sys.exit(0)

signal.signal(signal.SIGTERM, sig_handler)

while 1:
    time.sleep(1)

