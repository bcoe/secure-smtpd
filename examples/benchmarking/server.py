import asyncore,time
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
# termination of this process will kill worker children in process
# pool, so idle here...
while 1:
    time.sleep(1)
