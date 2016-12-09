'''
module : query_credentials

Provides the login crendentials to setup the query engine.
'''

from os import path
from os import environ
from .query import AQueryError

class AQueryCredentials(object):
    ''' Provides login and passwd for connection to a database.

    Login and Password are needed to connect to a data base. This provides
    a mechanism to pass that information by reading that information from
    $HOME/.bccreds. In this location two files need to be placed -

    passwd containing the password
    login containing the login id
    '''
    LOGIN = 'login'
    PASSWD = "passwd"
    BCCREDS = '.bccreds'
    
    def __init__(self):
        self._login = None
        self._passwd = None
        self._check_creds_cache()
        self._load_login()
        self._load_passwd()

    def _check_creds_cache(self):
        ''' Checks to see if a cache dir with the files exists
        
        Raises:
            AQueryError if the dir does not exist or doent containing
                the files needed for credentials.
        '''
        # Make sure $HOME is define
        if not "HOME" in environ:
            raise AQueryError('HOME environment variable must be define')
        home_dir = environ["HOME"]
        if not path.isdir(home_dir):
            raise AQueryError('''HOME environment variable points 
            to a location that does not exist''')
        bccreds_dir = path.join(home_dir, AQueryCredentials.BCCREDS)
        if not path.isdir(bccreds_dir):
            raise AQueryError('''.bccreds directory does not exist in the HOME
            location''')
        login_file = path.join(bccreds_dir, AQueryCredentials.LOGIN)
        if not path.isfile(login_file):
            raise AQueryError(''' A file named 'login' does not exist in the 
            .bccreds''')
        passwd_file = path.join(bccreds_dir, AQueryCredentials.PASSWD)
        if not path.isfile(passwd_file):
            raise AQueryError(''' A file names 'passwd' does not exist in the
            .bccreds director''')
    
    def _load_login(self):
        login_fd = open(path.join(path.join(environ['HOME'],
            AQueryCredentials.BCCREDS),AQueryCredentials.LOGIN),'r')
        # A trim is needed because a new line is entered by mistake
        self._login = (login_fd.read()).strip()
        login_fd.close()
    
    def _load_passwd(self):
        passwd_fd = open(path.join(path.join(environ['HOME'],
            AQueryCredentials.BCCREDS),AQueryCredentials.PASSWD),'r')
        self._passwd = (passwd_fd.read()).strip()
        passwd_fd.close()
    
    @property
    def login(self):
        return self._login
    
    @login.setter
    def login(self,login):
        raise AQueryError('Immutable property cannot be modified')
    
    @property
    def passwd(self):
        return self._passwd
    
    @passwd.setter
    def passwd(self,passwd):
        raise AQueryError('Immutable property cannot be modified')
    
    
        
        
        
        

        



