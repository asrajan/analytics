'''
module : query_result

This module defines the base class for all query result objects. Query result
objects own a result table.
'''
"""
module : Query
description: Defines a base calss for all queries
"""
from abc import ABCMeta,abstractmethod


class AQueryBase(object, metaclass=ABCMeta):
    """ A class representing the base class for all query results

    Results of a query is a table. This class encapsulates a table.

    Attributes:
       table : A list of lists that represents the result table. This can
                only be read after the query has been exected.
    """
    def __init__(self):
        self._table = None
        
    def __len__(self):
        return len(self._table)

    @property
    def table(self):
        if not self._table:
            raise RuntimeError("Cannot access un-initialized property")
        return self._table
    
    def has_run(self):
        if not self._table:
            return False
        return True

