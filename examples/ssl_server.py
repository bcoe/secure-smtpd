import secure_smtpd
import asyncore, logging
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
            credential_validator=FakeCredentialValidator()
        )
        asyncore.loop()

logger = logging.getLogger( secure_smtpd.LOG_NAME )
logger.setLevel(logging.INFO)
server = SSLSMTPServer()
server.start()