from secure_smtpd import SMTPServer

class SecureSMTPServer(SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, message_data):
        pass
        
server = SecureSMTPServer(('0.0.0.0', 1025), None)
server.run()
