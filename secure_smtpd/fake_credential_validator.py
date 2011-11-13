import secure_smtpd

# Implment this interface with an actual
# methodlogy for validating credentials, e.g.,
# lookup credentials for a usaer in Redis.
class FakeCredentialValidator(object):
    
    def validate(self, username, password):
        
        secure_smtpd.logger.warn('FakeCredentialValidator: you should replace this with an actual implementation of a credential validator.')
        
        if username == 'bcoe' and password == 'foobar':
            return True
        return False