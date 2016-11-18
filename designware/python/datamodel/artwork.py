""" This file creates the Artwork module

Artwork consists of a file or sett of files representing a copyrighted design
image
"""
from .error import AError
from datetime import date
from .name import *

class APattern(object):
    """ Defines the Pattern class

    Pattern represents a well defined string of known pattern type

    Attribute:
        pattern : A string representing the pattern
        id      : An integer representing the pattern
    """
    PATTERNS = ["","floral", "geometric", "paisley", "none"]
    def __init__(self,pattern):
        """ Constructor for pattern object

        Constructs a pattern object as a string
        
        Args:
            pattern : a string representing the pattern
        Raises:
            PatternError : If the string is not a valid pattern
        """
        self.__set_pattern(pattern)
    def index(self):
        """ Returns the id associated with the pattern
        """
        return self.idx
    def __repr__(self):
        """ String representation of the object 
        """
        return self.pattern
    def is_unknown(self):
        """ Returns true if the pattern is unknown"""
        return self.pattern == ""
    def __bool__(self):
        """ Returns false if the pattern is un known """
        return not self.is_unknown()
    def __set_pattern(self, pattern):
        """ Sets the pattern to the string input

        Sets the pattern to a string input. The pattern must be one of the
        known patterns or an empty string.

        Args:
            pattern : a string representing the pattern
        Raises:
            AError if the pattern entered is not a defined legal pattern.
        """
        if not pattern in APattern.PATTERNS:
            raise AError(pattern + ": is not defined")
        self.pattern = pattern
        self.idx = APattern.PATTERNS.index(pattern)

class AArtwork(object):
    """ Defines the Artwork base class.

    Artwork is an abstract class from which all artwork implementations must be
    derived from. Artwork represents a file or a group of files that represent
    a copyrighted image.

    Attributes:
        title : string representing a title for the Artwork
        studio : string representing the company that has a copyright
        designer : object representing the designer who created the artwork
        date_created : date of creation
        date_bought : date of buying
        patterns : A list of objects that represent patterns
        parents : A list of Artwork objects that inspeired this object
        children : A list of Artwork objects that are derived from this object
    """
    def __init__(self, title, studio, date_created):
        """ Constructor for an Artwork object

        At the time of the constructor, information about the studio, designer
        and title is known and must be provided.

        Args:
            title : string represnting the title
            studio : A studio object
            designer : object representing the name of the designer
        """
        self.title = title
        self.studio = AEntityName(studio)
        self.date_created = date.today()
        self.date_created.replace(date_created.year, date_created.month, 
                date_created.day)
        self.designer = []
        self.parents = []
        self.children = []
        self.patterns = []

    def is_designer_known():
        """ Returns trueif the designer for the artwork is known """
        return self.designer

    def set_designer(self, designer):
        """ Sets the creator or the author of the design 
        Args:
            designer : an object of type APerson Name
        """
        self.designer = designer

    def set_designer(self, fname, mname, lname):
        """ Sets the name of the designer from parts of the name

        Constructs a ApersonName object and attaches to the designer
        member of this class.

        Args:
            fname : A String first name
            mname : A string middle name
            lname : A string lname
        Raises:
            AError if the name is not correct
        """
        self.designer = APersonName(fname, mname, lname)

    def get_title(self):
        """ Returns the title of the image """
        return self.title

    def get_designer(self):
        return self.designer

    def get_studio(self):
        return self.studio

    def get_date_created(self):
        return self.date_created

