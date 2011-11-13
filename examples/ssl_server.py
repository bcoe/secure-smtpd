import asyncore
from smtpd_reloaded import SMTPServer

class SSLSMTPServer(SMTPServer):
    
    def __init__(self):
        pass
        
    def process_message(self, peer, mailfrom, rcpttos, message_data):
        print message_data
        
    def start(self):
        SMTPServer.__init__(self, ('0.0.0.0', 465), None, require_authentication=True, certfile='examples/server.crt', keyfile='examples/server.key')
        asyncore.loop()
        
server = SSLSMTPServer()
server.start()
