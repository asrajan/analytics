"""
module : AColQ

This module implements a column query object
"""

from query import AQuery

class AColQ(AQuery):
    """ Defines a column query.

    Creates a Query that returns column information of table in a 
    SQL database.

    Attributes:
        table_name : A string representing the name of the table
    """
    def __init__(self,table_name):
        """ Constructor for Column Query

        Args:
            table_name : A String table name
        """
        self._table_name = table_name
        super().__init__()

    @property
    def table_name(self):
        return self._table_name

    @table_name.setter
    def table_name(self, value):
        raise AQueryError("table_name cannot be updated after construction")

    def _init_query(self):
        """ Initialize the query string to extract column names """
        self._query = '''SELECT column_name 
        FROM information_schema.columns
        WHERE table_name=%s'''
        self._query_tuple = (self.table_name,)





    


