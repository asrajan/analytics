'''
module : filter

Filters the results of a query.
'''
from abc import ABCMeta,abstractmethod
from copy import copy

from .table import ATable
from .query import AQuery
from .query_base import AQueryBase

class AFilter(AQueryBase, metaclass=ABCMeta):
    ''' A query results filter.
    
    Provides a class abstraction for the data filtering process. Sometimes,
    it is more advantageous to perform additional filtering of the query
    results in python by leveraging python's libraries. This class provides
    an abstraction for that filtering.
    
    Note : It is inefficient to use this - When performance is of concern
    please use SQL directly
    
    Attributes :
        query : A reference to a AQuery object
        result : Result table
        reason : A Boolean attribute. If true the result also 
            contains result of filtering
    '''
    def __init__(self, query, reason=False):
        super().__init__()
        self._query = query
        self._reason = reason
    
    @property
    def reason(self):
        return self._reason
        
    @reason.setter
    def reason(self, reason):
        raise RuntimeError('Trying to set an immutable property')
        
        
    @property
    def query(self):
        return self._query
    
    @query.setter
    def query(self, query):
        raise RuntimeError('Trying to set an immutable property')
    
    
    def filter(self):
        ''' The filter method.
        
        Takes the results of a query and performs filter operation. 
        '''
        if not self._query._table:
            raise RuntimeError('Query has not been executed')
        self._table = ATable()
        if self._reason:
            self._table._columns = copy(self._query._table._columns)
            self._table._columns.append('Reason')
            self._table._types = copy(self._query._table._types)
            self._table._types.append(ATable.STRING)
        else:
            self._table._columns = self._query._table._columns
            self._table._types = self._query._table._types
        self._table._data = []
        self._filter()
        self._table._validate()
    
    @abstractmethod
    def _filter(self):
        pass
    