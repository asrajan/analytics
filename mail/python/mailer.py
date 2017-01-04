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
from abc                  import ABCMeta
from abc                  import abstractmethod

class AValidate(object, metaclass=ABCMeta):
    ''' A Class that can be validated.
    
    This is an abstract base class which provides a validate method
    that should be implemented.
    '''
    def __init__(self):
        pass
    
    def validate(self):
        ''' The public validate method that will be called by the client.'''
        if not self._validate():
            raise RuntimeError('Validation failed')
        return True
    
    @abstractmethod
    def _validate(self):
        pass
        

class AName(AValidate):
    ''' A class encapsulation of name
    
    A person's name that is used in an email greeting.
    
    Attributes:
        first : A string representing the first name
        last : A string representing the last name
        middle : A string representing the middle name
        nickname : A string representing a nick name
    '''
    def __init__(self, first, middle='', last='', nickname=''):
        super().__init__()
        self._first = first
        self._last = last
        self._middle = middle
        self._nickname = nickname
    
    @property
    def first(self):
        return self._first
    
    @property
    def last(self):
        return self._last
    
    @property
    def middle(self):
        return self._middle
        
    @property
    def nickname(self):
        return self._nickname
    
    @property
    def has_nickname(self):
        if self._nickname:
            return True
        else:
            return False
    
    @first.setter
    def first(self,first):
        raise RuntimeError('Can update a read-only property')
    
    @last.setter
    def last(self,last):
        raise RuntimeError('Can update a read-only property')
    
    @middle.setter
    def middle(self,middle):
        raise RuntimeError('Can update a read-only property')
    
    @nickname.setter
    def nickname(self,nickname):
        raise RuntimeError('Can update a read-only property')
    
    def _validate(self):
        return True
    
    
class AEmailAddress(AValidate):
    ''' A class encapsulation for email addresses '''
    def __init__(self, email_address):
        super().__init__()
        self._email_address = email_address
        
    def __str__(self):
        return self._email_address
    
    def __repr__(self):
        return self._email_address
    
    def _validate(self):
        return True

class ARelation(AValidate):
    ''' A Class that represents a relation ship '''
    RELATIONS = ['INTERNAL_CUSTOMER', 'EXTERNAL_CUSTOMER', 'INTERNAL']
    def __init__(self, relation):
        self._relation = relation
    def _validate(self):
        if self._relation in ARelation.RELATIONS:
            return True
        else:
            return False
        
class ARecepient(AValidate):
    ''' A class that describes an email recepient.
    
    A class encapsulation of email address, recepient name and relationship.
    '''
    def __init__(self, email_address = '', relation = 'INTERNAL_CUSTOMER', first = '', middle = '', last = '', nickname = ''):
        self._email_address = AEmailAddress(email_address)
        self._name = AName(first, middle, last, nickname)
        self._relation = ARelation(relation)
    
    @property
    def email_address(self):
        return self._email_address
        
    @property 
    def name(self):
        return self._name
    
    @property
    def relation(self):
        return self._relation
    
    def _validate(self):
        if not self._email_address.validate():
            return False
        if not self._name.validate():
            return False
        if not self._relation.validate():
            return False
        return True
                       
class AMailer(AValidate):
    ''' Implements a mail sending class
    
    Allows sending of mails programmatically with attachments from one 
    email address to another. The email address and the password are
    looked up using a credentials object so that the user does not have to
    specify the information in the client code.
    
    This is a poorman's solution - does not check for infinite bounce etc.
    
    TODO : Migrate to mailgun
    
    Attributes:
        recvs  : List of recepients
        files : List of files to send as attachments
        creds_dir : The credentials
        subject : String represent the subject line
        body    : Representing the body of the email
    '''        
    def __init__(self, creds_dir, subject='', body=''):
        self._creds_dir = creds_dir
        self._files = []
        self._recepients = []
        self._subject= subject
        self._body = body
            
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
    
    def _validate(self):
        ''' Validates the objects before firing the email '''
        for recepient in self._recepients:
            if not recepient.validate():
                return False
        return True
        
    def attach(self, file):
        ''' Adds a new attachment to the email '''
        if not path.isfile(file):
            raise RunTimeError(file + ' - Attachment file not found')
        self._files.append(file)
    
    def add_recepient(self, email_address, 
        relation = 'INTERNAL_CUSTOMER', 
        first = '',
        middle = '',
        last = '',
        nickname = ''):
        recepient = ARecepient(email_address, 
            relation,
            first,
            middle,
            last,
            nickname)
        self._recepients.append(recepient)                   
    
    def fire(self):
        ''' Does the actual work of firing the email '''
        # Reproduced from : 
        # http://stackoverflow.com/questions/3362600/how-to-send-email-attachments-with-python
        if not self.validate():
            return False
        creds = ACredentials(self.creds_dir)
        msg = MIMEMultipart()
        msg['From'] = creds.login   
        recepients = [str(recepient.email_address) for recepient in self._recepients]
        #msg['To'] needs a string
        msg['To'] = ', '.join(recepients)
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
        # recepients needs to be a list
        server.sendmail(creds.login, recepients, msg.as_string())
        server.quit()
        
        return True
        
        
        