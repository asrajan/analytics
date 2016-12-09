"""

module : table
description : This module models a table that is represented by a 
list of lists.

"""
class ATable(object):
    """ Represens a table.

    This class models a basic table that contains a heading for each column
    and has one ore more rows. It is ideally suited to transform into an
    excel sheet or could also represent a table from an SQL query.

    Attributes:
        _data : All the data rows in tne table - this could be represented
            as list of lists or as list of tuples. All entries of a column
            are of the same data type
        _columns : The list containing the heading of each column
        _types : This is an optional attribute that specifies the
        type of each column
    """
    STRING = 'string'
    NUMBER = 'number'
    DATETIME = 'datetime'
    ROWID = 'rowid'
    BINARY = 'binary'
    def __init__(self):
        self._columns = None
        self._types = None
        self._data = None

    @property
    def columns(self):
        if not self._columns:
            raise RuntimeError("Cannot access an uninitialized field.")
        return self._columns

    @columns.setter
    def columns(self, columns):
        raise RuntimeError("This field represents a result of a query.")

    @property
    def data(self):
        if not self._data:
            raise RuntimeError("Cannot access an uninitialized field")
        return self._data

    @data.setter
    def data(self, data):
        raise RuntimeError("This is a readonly field")

    @property
    def types(self):
        return self._types
    
    @types.setter
    def types(self, types):
        raise RuntimeError('This is a read-only field')
        
    def _validate(self):
        """ Validates that the table is well formed

        A table is well-formed if all the elements of the columns are 
        strings.

        The number of elements in the heading/columns is the same as the
        number of elements of each row of the data. The type of each row
        of the data is consistent across all rows. A None type will match
        with any other type.
        
        """
        num_cols = len(self.columns)
        if not len(self.data):
            return True # An empty table is valid
        type_list = [type(x) for x in self.data[0]]
        for row in self.data[1:]:
            for idx,x in enumerate(zip(type_list,row)):
                if x[1] == None:
                    continue
                if x[0] == type(None):
                    type_list[idx] = type(x[1])
                    continue
                if x[0] != type(x[1]):
                    raise RuntimeError("Type error in row " + idx)
        return True # Data base is consistent








