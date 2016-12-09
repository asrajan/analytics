"""
module: query_engine

Executes queries and returns th results in the query objevt
"""
import pymssql
from pymssql import _mssql
import pprint
from .query import AQuery
from .query import AQueryError
from .table import ATable
import logging

class AQueryEngine(object):
    """ Implements the query engine.

    This class accepts queries and returns their results. It also manages 
    how queries may get executed.

    Note : This is an abstraction of the algorithm used to execute queries
    against a data base. For now the algorithm used is first-come first-served
    and blocking.

    Note : The connection object in DB API 2.0 has __del__ method that closes
    the connection. So we do not have to explicitly close the connection here

    RAII: In python RAII has to be done using the with clause only.

    Attributes:
        server   : string name of the SQL Server instance
        user     : string name of the user
        password : string name of the user
        database : string name of the database to connect to
        port     : integer port over which the server is listening 
        conn     : A per QueryEngine connection object
    """
    def __init__(self, server, user, password, database, port):
        self._server = server
        self._user = user
        self._password = password
        self._database = database
        self._port = port
        self._conn = None
        self._init_conn()

    def _init_conn(self):
        """ Initialize connection object

        Raises:
            A number of different connection errors
        """
        if not self._conn:
            self._conn = pymssql.connect(
            server=self._server,
            user=self._user,
            password=self._password,
            database=self._database,
            timeout=0,
            login_timeout=60,
            charset='UTF-8',
            as_dict=False,
            host='',
            appname=None,
            port=self._port,
            autocommit=False)
        else:
            raise AQueryError("Connection can only be made once")

    def _translate_type_code(self, type_code):
        ''' Given a type code returns a string description of the type.
        
        DB-API specifies a list of types for each column. This gives
        a string representation that can be used by objects downstream
        in the Data Pipeline without adding dependencies to DB-API.
        '''
        if type_code == pymssql.STRING:
            return 'string'
        if type_code == pymssql.NUMBER:
            return 'number'
        if type_code == 5: # Handle Row ID as a Number
            return 'number'
        if type_code == pymssql.DATETIME:
            return 'datetime'
        if type_code == pymssql.BINARY:
            return 'binary'
        raise AQueryError('Undefined type_code ' + str(type_code)) 
            
        
    def execute(self,query):
        """ Executes a query as specified by the query object. This
        query is executed against the AQueryEngine owned connection
        and is blocking.

        Note : Results of the entire query is returned in one shot -
        client needs to ensure that the result is not very huge.

        Note: description attribute returns a lits of tuples where
        each tuple describes the columns.

        Args :
            query : A query object
        """
        cursor = self._conn.cursor()
        logging.info(query._query)
        cursor.execute(query.query, query.query_tuple)

        desc = cursor.description
        # Return it as list and not as tuples
        # Note : This implies mutability that seems worng but is useful
        # for minor data massaging without allocation.
        cols = []
        types = []
        for col in desc:
            cols.append(col[0])
            types.append(self._translate_type_code(col[1]))
        
        # We populate the private methods of the table
        # We short circuit the property APIS
        # TODO : What is the python way for friends
        results = ATable()
        results._columns = cols
        results._types = types
        rows = cursor.fetchall()
        data= []
        for row in rows:
            data.append(
                [a.strip() if isinstance(a,str) else a for a in row])

        results._data = data
        # Park the table into the query objecty for further processing
        query._table = results






