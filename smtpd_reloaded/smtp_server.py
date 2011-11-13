import ssl, smtpd, time, asyncore
from smtp_channel import SMTPChannel
from multiprocessing import Process
from multiprocessing import Process, Queue
from Queue import Empty
from asyncore import ExitNow

class SMTPServer(smtpd.SMTPServer):
        
    def __init__(self, localaddr, remoteaddr, certfile=None, keyfile=None, ssl_version=ssl.PROTOCOL_SSLv23, require_authentication=False):
        smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_version = ssl_version
        self.process_lookup = {}
        self.current_process_id = 0
        self.queue = Queue()
        self.require_authentication = require_authentication
        
    def handle_accept(self):
        self.current_process_id += 1
        
        process = Process(target=self._accept_subprocess, args=[self.queue, self.current_process_id])
        process.start()
        
        self.process_lookup[self.current_process_id] = process
        self._terminate_completed_subprocesses()
        
    def _terminate_completed_subprocesses(self):
        try:
            while True:
                process_id = self.queue.get(block=True, timeout=0.01)
                self.process_lookup[process_id].terminate()
        except Empty:
            pass
        
    def _accept_subprocess(self, queue, process_id):
        try:
            pair = self.accept()
            if pair is not None:
                newsocket, fromaddr = pair
                if self.certfile:
                    newsocket = ssl.wrap_socket(
                        newsocket,
                        server_side=True,
                        certfile=self.certfile,
                        keyfile=self.keyfile,
                        ssl_version=self.ssl_version
                    )
                channel = SMTPChannel(self, newsocket, fromaddr, require_authentication=self.require_authentication)
                asyncore.loop()
        except ExitNow:
            queue.put(process_id)