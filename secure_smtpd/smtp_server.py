import secure_smtpd
import ssl, smtpd, time, asyncore
from smtp_channel import SMTPChannel
from multiprocessing import Process
from multiprocessing import Process, Queue
from Queue import Empty
from asyncore import ExitNow

class SMTPServer(smtpd.SMTPServer):
        
    def __init__(self, localaddr, remoteaddr, ssl=False, certfile=None, keyfile=None, ssl_version=ssl.PROTOCOL_SSLv23, require_authentication=False, credential_validator=None, debug=False):
        smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)
        self.debug = debug
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_version = ssl_version
        self.process_lookup = {}
        self.current_process_id = 0
        self.queue = Queue()
        self.require_authentication = require_authentication
        self.credential_validator = credential_validator
        self.ssl = ssl
        
    def handle_accept(self):
        self.current_process_id += 1
        
        if self.debug:
            secure_smtpd.logger.info('handle_accept(): called.')
        
        process = Process(target=self._accept_subprocess, args=[self.queue, self.current_process_id])
        process.start()
        
        self.process_lookup[self.current_process_id] = process
        self._terminate_completed_subprocesses()
        
    def _terminate_completed_subprocesses(self):
        try:
            while True:
                process_id = self.queue.get(block=True, timeout=0.01)
                self.process_lookup[process_id].terminate()
                
                if self.debug:
                    secure_smtpd.logger.info('_terminate_completed_subprocesses(): subprocess %d terminated.' % process_id)
                
        except Empty:
            pass
        
    def _accept_subprocess(self, queue, process_id):
        try:
            pair = self.accept()
            
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
                    debug=self.debug
                )
                
                if self.debug:
                    secure_smtpd.logger.info('_accept_subprocess(): starting asyncore within subprocess.')
                
                asyncore.loop()
                secure_smtpd.logger.error('_accept_subprocess(): asyncore loop exited.')
        except ExitNow:
            if self.debug:
                secure_smtpd.logger.info('_accept_subprocess(): smtp channel terminated asyncore.')
            queue.put(process_id)