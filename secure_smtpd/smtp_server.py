import secure_smtpd
import ssl, smtpd, time, asyncore, os
from smtp_channel import SMTPChannel
from multiprocessing import Process
from asyncore import ExitNow

class SMTPServer(smtpd.SMTPServer):
    
    KILL_SIGNAL = 9
    MAXIMUM_EXECUTION_TIME = 2
        
    def __init__(self, localaddr, remoteaddr, ssl=False, certfile=None, keyfile=None, ssl_version=ssl.PROTOCOL_SSLv23, require_authentication=False, credential_validator=None, debug=False):
        smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)
        self.debug = debug
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_version = ssl_version
        self.subprocesses = []
        self.require_authentication = require_authentication
        self.credential_validator = credential_validator
        self.ssl = ssl
        
    def handle_accept(self):
        if self.debug:
            secure_smtpd.logger.info('handle_accept(): called.')
        
        process = Process(target=self._accept_subprocess, args=[])
        self.subprocesses.append({
            'process': process,
            'start_time': time.time()
        })
        process.start()
        
        self._terminate_expired_subprocesses()
        
    def _terminate_expired_subprocesses(self):
        current_time = time.time()
        
        def alive(process_dict):
            if (current_time - process_dict['start_time']) > self.MAXIMUM_EXECUTION_TIME:
                return False
            return process_dict['process'].is_alive()
            
        self.subprocesses = filter(alive, self.subprocesses)
        
    def _accept_subprocess(self):
        try:
            pair = self.accept()
            map = {}
            
            if self.debug:
                secure_smtpd.logger.info('_accept_subprocess(): smtp connection accepted within subprocess.')
            
            if pair is not None:
                newsocket, fromaddr = pair
                if self.ssl:
                    newsocket = ssl.wrap_socket(
                        newsocket,
                        server_side=True,
                        certfile=self.certfile,
                        keyfile=self.keyfile,
                        ssl_version=self.ssl_version,
                    )
                channel = SMTPChannel(
                    self,
                    newsocket,
                    fromaddr,
                    require_authentication=self.require_authentication,
                    credential_validator=self.credential_validator,
                    debug=self.debug,
                    map=map
                )
                
                if self.debug:
                    secure_smtpd.logger.info('_accept_subprocess(): starting asyncore within subprocess.')
                
                asyncore.loop(map=map)
                secure_smtpd.logger.error('_accept_subprocess(): asyncore loop exited.')
        except ExitNow:
            if self.debug:
                secure_smtpd.logger.info('_accept_subprocess(): smtp channel terminated asyncore.')
            os.kill( os.getpid(), self.KILL_SIGNAL )