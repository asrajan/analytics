""" This file creates the Artwork module

Artwork consists of a file or sett of files representing a copyrighted design
image
"""
from .error import AError
from datetime import date
from .name import *
from os import path

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
        self._set_pattern(pattern)
    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        raise AError("index property is not writable")
    
    @property
    def pattern(self):
        return self._pattern
    
    @pattern.setter
    def pattern(self,pattern):
        self._set_pattern(pattern)

    def __repr__(self):
        return self._pattern

    def is_unknown(self):
        return self._pattern == ""

    def __bool__(self):
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
        self._pattern = pattern
        self._index = APattern.PATTERNS.index(pattern)

class AArtwork(object):
    """ Defines the Artwork base class.

    Artwork is an abstract class from which all artwork implementations must be
    derived from. Artwork represents a file or a group of files that represent
    a copyrighted image.

    Attributes:
        name           : A string identifier for the artwork as given by the 
                         company that is the current owner of the artwork 
        studio         : AEntityName object representing the name of the studio
        designer       : APersonName object representing the designer 
        date_created   : datetime.date object representing date of creation
        date_bought    : datetime.date object representing date of buying
        patterns       : A List of APattern objects where each object represents 
                         a pattern
        parents        : A List of AArtwork objects that inspired this Artwork objects
        children       : A List of AArtwork objects that are derived from this object
        uri            : A folder containing all the images for a given artwork
        original_name  : A string identifier for the artwork as given by the
                         studio
        cost           : In dollars(double)
        files          : A dictionary of files with the keys
                FULL   - The name of the FULL file
                FLAT   - The name of the flat file
                LAYERS -  A list of layers

    """
    FULL = "FULL"
    FLAT = "FLAT"
    LAYERS = "LAYERS"
    INDEX = "INDEX"
    def __init__(self, name, studio, date_created):
        """ Constructor for an Artwork object

        At the time of the constructor, information about the studio, designer
        and title is known and must be provided.

        Args:
            title : string represnting the title
            studio : A studio object
            designer : object representing the name of the designer
        """
        self._name = name
        self._studio = AEntityName(studio)
        self._date_created = date.today()
        self._date_created.replace(date_created.year, date_created.month, 
                date_created.day)
        self._date_bought = None
        self._designer = None
        self._parents = None
        self._children = None
        self._patterns = None
        self._original_name = None
        self._files = dict()
        self._cost = None
        self._uri = None

    @property
    def studio(self):
        return self._studio

    @studio.setter
    def studio(self, studio):
        raise AError("Studio must be set at construction ")

    @property
    def date_created(self):
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        raise AError("Creation date must be set during construction")

    @property
    def date_bought(self):
        if not self._date_bought:
            return self._date_created
        else:
            return self._date_bought

    @date_bought.setter
    def date_bought(self, date_bought):
        if not self._date_bought:
            self._date_bought = date_bought
        else:
            raise AError("Cannot set date_bought multiple times")

    @property
    def designer(self):
        return self._designer

    @designer.setter
    def designer(self,designer):
        if not self._designer:
            self._designer = designer
        else:
            raise AError("Designer already set")
  
    def is_designer_known():
        """ Returns true if the designer for the artwork is known """
        if self._designer:
            return True
        else:
            return False

    def set_designer(self, fname, mname, lname):
        """ Sets the name of the designer from parts of the name

        Args:
            fname : A String first name
            mname : A string middle name
            lname : A string lname
        Raises:
            AError if the name is not correct
        """
        self._designer = APersonName(fname, mname, lname)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not self._name:
            self._name = name
        else:
            raise AError("Artwork name can only be set once")
    
    @property
    def original_name(self):
        return self._original_name
    
    @original_name.setter
    def original_name(self, original_name):
        if not self._original_name:
            self._original_name = original_name
        else:
            raise AError("Attempting to modify an original name")

    @property
    def flat_file(self):
        return self._files[AArtwork.FLAT]

    @flat_file.setter
    def flat_file(self, flat_file):
        if AArtwork.FLAT in self._files:
            raise AError("Flat file has already been set")
        else:
            self._files[AArtwork.FLAT] = flat_file

    @property
    def index_files(self):
        return self._files[AArtwork.INDEX]

    @index_files.setter
    def index_files(self):
        raise AError("Use append_index_file instead")

    def append_index_file(self, index_file):
        if not AArtwork.INDEX in self._files:
            self._files[AArtwork.INDEX] = list()
        self._files[AArtwork.INDEX].append(index_file)

    @property
    def full_file(self):
        return self._files[AArtwork.FULL]

    @full_file.setter
    def full_file(self, full_file):
        if AArtwork.FULL in self._files:
            raise AError("Cannot set full_file to " + full_file)
        else:
            self._files[AArtwork.FULL] = full_file

    def append_layer_file(self, file):
        if not AArtwork.LAYERS in self._files:
            self._files[AArtwork.LAYERS] = list()
        self._files[AArtwork.LAYERS].append(file)

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, cost):
        if not self._cost:
            self._cost = double(cost)
        else:
            raise AError("Cost already set")

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        if not self._uri:
            if path.exists(uri):
                self._uri = uri
            else:
                AError("uri specified does not exist")
        else:
                AError("uri is already set")
           


        
