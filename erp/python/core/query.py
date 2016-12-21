"""
module : Query
description: Defines a base calss for all queries
"""
from abc import ABCMeta,abstractmethod
from .query_base import AQueryBase

class AQueryError(Exception):
    """ This is the base class for all exceptions raised in the framework

    Attributes:
        message : string carrying the error message
    """
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return self.message

    def __str__(self):
        return self.message

class AQuery(AQueryBase, metaclass=ABCMeta):
    """ A class representation for SQL query

    Encapsulates the query string as well as the result of the query. These
    queries are made to the ERP data base to extract information about the 
    SKUs. The ERP data base is generally an SQL data base.

    Attributes:
       query : A string representing an SQL query. This is generally a read
                only attribute.
       query_tuple : A String representing the query tuple
       table : A list of lists that represents the result table. This can
                only be read after the query has been exected.
    """
    def __init__(self):
        super().__init__()
        self._query = ""
        self._query_tuple = ()
        self._init_query()
        if not self._query:
            raise RuntimeError("Query not set")

    @property
    def query(self):
        return self._query
    
    @query.setter
    def query(self,query):
        raise RuntimeError("Property not writable")
    
    @property
    def query_tuple(self):
        return self._query_tuple

    @abstractmethod
    def _init_query(self):
        pass

