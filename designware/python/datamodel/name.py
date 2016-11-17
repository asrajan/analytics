""" This module defines different types of name classes """
from abc import ABCMeta, abstractmethod
from .error import AError

class AName(object, metaclass=ABCMeta):
    """ An abstract base class for names """
    @abstractmethod
    def __repr__(self):
        pass
    @abstractmethod
    def __str__(self):
        pass

class APersonName(AName):
    """ Defines the name of a person 

    Persons generally have three names, first name, middle name and last name

    Attributes:
        fname : string representing the first name
        mname : string representing the middle name
        lname : string representing the last name
    """
    def __init__(self, fname, mname, lname):
        """ Constructor for the name 

        Args:
            fname : string for the first name
            mname : string for the middle name
            lname : sring for the last name
        Raises:
            AError if name is incorrect
        """
        if (not fname) and (not lname):
            raise AError("A person must have either first or last name")
        self.mname = str(mname)
        self.fname = str(fname)
        self.lname = str(lname)
    def first_name(self):
        """ Returns the first name of a person """
        return self.fname
    def last_name(self):
        """ returns the last name of a person """
        return self.lname
    def middle_name(self):
        """ Returns the middle name of a person """
        return self.mname
    def __repr__(self):
        """ Returns a string representing the name """
        names = [self.fname, self.mname, self.lname]
        names = [n for n in names if n] 
        full_name = " ".join(names)
        return full_name 
    def __str__(self):
        return self.__repr__()
