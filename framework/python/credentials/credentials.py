'''
module : credentials

Provides the login crendentials to setup services.
'''

from os import path
from os import environ

class ACredentials(object):
    ''' Poorman's credentials to allow use fo different services

    A varety of different services require login and password. This provides
    a mechanism by which the client does not have to specify the login and
    password in the script. This provides a level of security equivalent to
    the security available in a local compute resource.
    
    Attributes:
        login : String representing the login id or the user name
        passwd : String representing the password
        creds_dir : String representing the directory in which the 
            credentials are stored.
        
    '''
    LOGIN = 'login'
    PASSWD = "passwd"
    
    def __init__(self, creds_dir):
        self._login = None
        self._passwd = None
        self._creds_dir = creds_dir
        self._check_creds_cache()
        self._load_login()
        self._load_passwd()

    def _check_creds_cache(self):
        ''' Checks to see if a cache dir with the files exists
        
        Raises:
            RuntimeError if the dir does not exist or doent containing
                the files needed for credentials.
        '''
        # Make sure $HOME is define
        if not "HOME" in environ:
            raise RuntimeError('HOME environment variable must be define')
        home_dir = environ["HOME"]
        if not path.isdir(home_dir):
            raise RuntimeError('''HOME environment variable points 
            to a location that does not exist''')
        bccreds_dir = path.join(home_dir, self._creds_dir)
        if not path.isdir(bccreds_dir):
            raise RuntimeError('''.bccreds directory does not exist in the HOME
            location''')
        login_file = path.join(bccreds_dir, ACredentials.LOGIN)
        if not path.isfile(login_file):
            raise RuntimeError(''' A file named 'login' does not exist in the 
            .bccreds''')
        passwd_file = path.join(bccreds_dir, ACredentials.PASSWD)
        if not path.isfile(passwd_file):
            raise RuntimeError(''' A file names 'passwd' does not exist in the
            .bccreds director''')
    
    def _load_login(self):
        login_fd = open(path.join(path.join(environ['HOME'],
            self._creds_dir),ACredentials.LOGIN),'r')
        # A trim is needed because a new line is entered by mistake
        self._login = (login_fd.read()).strip()
        login_fd.close()
    
    def _load_passwd(self):
        passwd_fd = open(path.join(path.join(environ['HOME'],
            self._creds_dir),ACredentials.PASSWD),'r')
        self._passwd = (passwd_fd.read()).strip()
        passwd_fd.close()
    
    @property
    def login(self):
        return self._login
    
    @login.setter
    def login(self,login):
        raise RuntimeError('Immutable property cannot be modified')
    
    @property
    def passwd(self):
        return self._passwd
    
    @passwd.setter
    def passwd(self,passwd):
        raise RuntimeError('Immutable property cannot be modified')
    
    @property
    def creds_dir(self):
        return self._creds_dir
    
    @creds_dir.setter
    def creds_dir(self, value):
        raise RuntimeError('Immutable property cannot be modified')
    
    
        
        
        
        

        



