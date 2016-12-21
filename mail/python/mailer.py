'''
module : mailer

Provides a minimal layer of abstraction to send mails with attachments from
one account to another.

Note : Currently supports sending from GMAIL only
'''

from credentials          import ACredentials

from os import path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base      import MIMEBase
from email.mime.text      import MIMEText
from email.utils          import COMMASPACE
from email.utils          import formatdate
from email                import encoders
 

class AMailer(object):
    ''' Implements a mail sending class
    
    Allows sending of mails programmatically with attachments from one 
    email address to another. The email address and the password are
    looked up using a credentials object so that the user does not have to
    specify the information in the client code.
    
    This is a poorman's solution - does not check for infinite bounce etc.
    
    TODO : Migrate to mailgun
    
    Attributes:
        recv  : String representing the email address of the recepient
        files : List of files to send as attachments
        creds_dir : The credentials
        subject : String represent the subject line
        body    : Representing the body of the email
    '''        
    def __init__(self, recv, creds_dir, subject='', body=''):
        self._recv = recv
        self._creds_dir = creds_dir
        self._files = []
        self._subject= subject
        self._body = body
    
    @property
    def recv(self):
        return self._recv
    @recv.setter
    def recv(self, recv):
        raise RuntimeError('Immutable property cannot be modified')
        
    @property
    def creds_dir(self):
        return self._creds_dir
    @creds_dir.setter
    def creds_dir(self, creds_dir):
        raise RuntimeError('Immutable property cannot be modified')
        
    @property
    def subject(self):
        return self._subject
    @subject.setter
    def subject(self, subject):
        raise RuntimeError('Immutable property cannot be modified')
        
    @property
    def body(self):
        return self._body
    @body.setter
    def body(self, body):
        raise RuntimeError('Immutable property cannot be modified')
    
    def attach(self, file):
        ''' Adds a new attachment to the email '''
        if not path.isfile(file):
            raise RunTimeError(file + ' - Attachment file not found')
        self._files.append(file)
    
    
    
    def fire(self):
        ''' Does the actual work of firing the email '''
        # Reproduced from : 
        # http://stackoverflow.com/questions/3362600/how-to-send-email-attachments-with-python
        creds = ACredentials(self.creds_dir)
        msg = MIMEMultipart()
        msg['From'] = creds.login
        msg['To'] = self.recv
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = self.subject
        msg.attach( MIMEText(self.body) )

        for f in self._files:
            part = MIMEBase('application', "octet-stream")
            fd = open(f,'rb')
            part.set_payload( fd.read() )
            fd.close()
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 
            'attachment; filename="{0}"'.format(path.basename(f)))
            msg.attach(part)
        
        
        
        # Reproduced from : http://naelshiab.com/tutorial-send-email-python/
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(creds.login, creds.passwd)
        server.sendmail(creds.login, 'asrajan@gmail.com', msg.as_string())
        server.quit()
        
        
        