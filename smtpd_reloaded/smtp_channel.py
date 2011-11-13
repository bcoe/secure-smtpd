import smtpd
import base64
from asyncore import ExitNow
from smtpd import DEBUGSTREAM, NEWLINE, EMPTYSTRING, COMMASPACE

class SMTPChannel(smtpd.SMTPChannel):
    
    EXTENSIONS = [
        'AUTH LOGIN'
    ]
    CHALLENGE = 'challenge string'
    
    def __init__(self, smtp_server, newsocket, fromaddr, require_authentication=False):
        smtpd.SMTPChannel.__init__(self, smtp_server, newsocket, fromaddr)
        self.require_authentication = require_authentication
        self.authenticating = False
        self.authenticated = False
        self.username = None
        self.password = None
    
    def smtp_QUIT(self, arg):
        self.push('221 Bye')
        self.close_when_done()
        raise ExitNow()
        
    def collect_incoming_data(self, data):
        self.__line.append(data)
    
    def smtp_EHLO(self, arg):
        if not arg:
            self.push('501 Syntax: HELO hostname')
            return
        if self.__greeting:
            self.push('503 Duplicate HELO/EHLO')
        else:
            self.push('250-%s Hello %s' %  (self.__fqdn, arg))
            for extension in self.EXTENSIONS:
                self.push('250-%s' % extension)
            self.push('250 EHLO')
    
    def smtp_AUTH(self, arg):
        if 'LOGIN' in arg:
            self.authenticating = True
            split_args = arg.split(' ')
            
            if len(split_args) == 2:
                self.username = base64.b64decode( arg.split(' ')[1] )
                self.push('334 ' + base64.b64encode('Username'))
            else:
                self.push('334 ' + base64.b64encode('Username'))
                
        elif not self.username:
                self.username = base64.b64decode( arg )
                self.push('334 ' + base64.b64encode('Password'))
        else:
            self.authenticating = False
            self.password = base64.b64decode(arg)
            if self.username == 'bcoe' and self.password == 'pass':
                self.authenticated = True
                self.push('235 Authentication successful.')
            else:
                self.push('454 Temporary authentication failure.')
            
    def found_terminator(self):
        line = EMPTYSTRING.join(self.__line)
        #print >> DEBUGSTREAM, 'Data:', repr(line)
        self.__line = []
        if self.__state == self.COMMAND:
            if not line:
                self.push('500 Error: bad syntax')
                return
            method = None
            i = line.find(' ')
            
            if self.authenticating:
                arg = line.strip()
                command = 'AUTH'
            elif i < 0:
                command = line.upper()
                arg = None
            else:
                command = line[:i].upper()
                arg = line[i+1:].strip()
            
            if not command in ['AUTH', 'EHLO', 'HELO', 'NOOP', 'RSET', 'QUIT']:
                if self.require_authentication and not self.authenticated:
                    self.push('530 Authentication required')
                    
            method = getattr(self, 'smtp_' + command, None)
            if not method:
                self.push('502 Error: command "%s" not implemented' % command)
                return
            method(arg)
            return
        else:
            if self.__state != self.DATA:
                self.push('451 Internal confusion')
                return
            # Remove extraneous carriage returns and de-transparency according
            # to RFC 821, Section 4.5.2.
            data = []
            for text in line.split('\r\n'):
                if text and text[0] == '.':
                    data.append(text[1:])
                else:
                    data.append(text)
            self.__data = NEWLINE.join(data)
            status = self.__server.process_message(
                self.__peer,
                self.__mailfrom,
                self.__rcpttos,
                self.__data
            )
            self.__rcpttos = []
            self.__mailfrom = None
            self.__state = self.COMMAND
            self.set_terminator('\r\n')
            if not status:
                self.push('250 Ok')
            else:
                self.push(status)
