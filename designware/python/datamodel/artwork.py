""" This file creates the Artwork module

Artwork consists of a file or sett of files representing a copyrighted design
image
"""
from error import AError 

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
        if not pattern in APattern.PATTERNS:
            raise AError(pattern + ": is not defined")
        self.pattern = pattern
        self.id = APattern.PATTERNS.index(pattern)

    def id(self):
        """ Returns the id associated with the pattern
        """
        return self.id
    
    def __repr__(self):
        """ String representation of the object 
        """
        return self.pattern


class AArtwork(object):
    """ Defines the Artwork base class.

    Artwork is an abstract class from which all artwork implementations must be
    derived from. Artwork represents a file or a group of files that represent
    a copyrighted image.

    Attributes:
        title : string representing a title for the Artwork
        studio : object representing the company that has a copyright
        designer : object representing the designer who created the artwork
        patterns : A list of objects that represent patterns
        parents : A list of Artwork objects that inspeired this object
        children : A list of Artwork objects that are derived from this object
    """
    def __init__(self, title, studio, designer):
        """ Constructor for an Artwork object

        At the time of the constructor, information about the studio, designer
        and title is known and must be provided.

        Args:
            title : string represnting the title
            studio : A studio object
            designer : object representing the name of the designer
        """
        self.title = title
        self.studio = studio
        self.designer = designer
        self.parents = []
        self.children = []
        self.patterns = []
