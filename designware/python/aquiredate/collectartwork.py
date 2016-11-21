"""
Filename : collectartwork.py

Collects information on artwork images from a Artwork Designs folder
at envogue.

At envogue Artwork Designs folder houses all information about various artwork
that have been bought over the years. It includes the flat files, textured
files, layers etc. This has been organically created by various designers. This module attempts to build a data base in memory mapping artwork directory with files that form the artwork. 
"""
from datamodel.error import AError
from datamodel.artwork import AArtwork
from datamodel.artworkbuilder import AArtworkBuilder
import os
from os import path
import re
from abc import ABCMeta, abstractmethod
from datetime import date

class ACollect(object):
    """ Builds a list of artwork objects based on envogue artwork collection.

    Within Envogue nternational all the bought artwork is stored at:
    M:\Design Studios\Artwork Design\2016-11-02 6 DESIGNS\STRATTON\

    In the above folder path the following information is encoded

    Folder Name : 2012-01 - AVIGNON
    In the above folder name AVIGNON is title
    2012-01 is the date when it was aquired
    Studion name is not known.

    Attributes :
        root_dir : The root directory from which to begin the search
        __dir_tree : Builds a directory tree by walking the root_dir
    """
    def __init__(self, root_dir):
        """ Constructs the AArtworkListBuilder """
        self.root_dir = root_dir
        self.tiff_db = {}
        if not path.exists(self.root_dir):
            raise AError(root_dir + " does not exist on system. Please check.")
        if not path.isdir(self.root_dir):
            raise AError(self.root_dir + " is not a folder/directory.")
        
    def collect(self):
        """ The engine for visiting the directories. """
        for root, dirs, files in os.walk(self.root_dir):
            tiff_file_exists = False
            for file in files:
                if ACollect.__is_tiff(file):
                    tiff_file_exists = True
                    break
            p = ACollect.__categorize(root)
            if not p:
                print("!!!! Could not categorize : %s !!!!"%(root))
            else: 
                builder = AArtworkBuilder()
                if p.title:
                    builder.set_title(p.title)
                if p.date:
                    builder.set_date_created(p.date)
                if p.studio:
                    builder.set_studio(p.studio)
                else:
                    builder.set_studio("Unknown Company")
                builder.get_artwork()



    def __is_tiff(filename):
        """ Returns true if the file name conforms to a tiff file. 

        This method returns true if the file name matches a tiff file format.
        Args:
            filename : string representing the file
        """
        pattern = re.compile('.*\\.tif+$')
        if pattern.fullmatch(filename) : 
            return True
        return False

    def __categorize(dirname):
        """ Categorize the directory containing a tiff file 

        Based on the name of the directory it is possible to extract
        information such as buy date and name of the studio.
        
        Note : These patterns have to be layered carefully
        Pattern 1 : YYYY-MM - STUDIO
        Pattern 2 : YYYY-MM STUDIO
        Pattern 3 : YYYY-MM-DD STUDIO
        pattern2 = re.compile('(\\d{4})\\s*-\\s*(\\d{2})\\s*[a-zA-Z](\\w.*)$');
        pattern3 = re.compile('(\\d{4})\\s*-\\s*(\\d{2})\\s*-\\s*(\\d+)\\s*[a-zA-Z](\\w.*)$');

        Args:
            dirname : a string representing the directory containing the file
        """
        patterns = [ADFP1, ADFP2, ADFP3, ADFP4]
        for pattern in patterns:
            p = pattern(dirname)
            if p():
                return p
        return False


class ADataFromPattern(object, metaclass=ABCMeta):
    """ Base class for etctracting Artwork data from the directory name 

    The metadata associated with the artwork is sometimes embedded in the
    dirname pattern. This class forms the base class for doing that work of
    extraction.
    
    """
    def __init__(self, dirname):
        self.dirname = dirname
        self.title = []
        self.date = []
        self.studio = []
    @abstractmethod
    def pattern(self):
        pass
    @abstractmethod
    def __call__(self):
        pass
    @abstractmethod
    def succ(self):
        pass
    def __str__(self):
        return "Title : " + self.title + " Date: " + date
    def __repr__(self):
        return "Title : " + self.title + " Date: " + date
    def succ(self):
        print("*** Categorized %s as %s ***"%(self.dirname, self.pattern()))

class ADFP1(ADataFromPattern):
    """ Extracts information from directorieswith the following pattern :

        Pattern 1 : YYYY-MM - STUDIO
    """    
    __PATTERN = re.compile('(\\d{4})\\s*-\\s*(\\d{2})\\s*-\\s*([a-zA-Z][^\\\\]*)$');
    def __init__(self, dirname):
        super().__init__(dirname)
    def __call__(self):
        match = ADFP1.__PATTERN.search(self.dirname)
        if match:
            self.date = date(int(match.group(1)),int(match.group(2)), 1)
            self.title = match.group(3)
            return True
        return False
    def pattern(self):
        return "PATTERN1"

class ADFP2(ADataFromPattern):
    """ Extracts information from directorieswith the following pattern :

        Pattern 2 : YYYY-MM STUDIO
    """   
    __PATTERN = re.compile('(\\d{4})\\s*-\\s*(\\d{2})\\s*([a-zA-Z][^\\\\]*)$');
    def __init__(self, dirname):
        super().__init__(dirname)
    def __call__(self):
        match = ADFP2.__PATTERN.search(self.dirname)
        if match:
            self.date = date(int(match.group(1)),int(match.group(2)), 1)
            self.title = match.group(3)
            return True
        return False
    def pattern(self):
        return "PATTERN2"

class ADFP3(ADataFromPattern):
    """ Extracts information from directorieswith the following pattern :

        Pattern 3 : YYYY-MM STUDIO
    """   
    __PATTERN = re.compile('(\\d+)\\s*-\\s*(\\d+)\\s*-\\s*(\\d+)\\s*([a-zA-Z][^\\\\]*)$');
    def __init__(self, dirname):
        super().__init__(dirname)
    def __call__(self):
        match = ADFP3.__PATTERN.search(self.dirname)
        if match:
            self.date = date(int(match.group(1)),
                    int(match.group(2)), int(match.group(3)))
            self.title = match.group(3)
            return True
        return False
    def pattern(self):
        return "PATTERN3"

class ADFP4(ADataFromPattern):
    """ Extracts information from directories with the following pattern :

        Pattern 4 : YYYY-MM STUDIO
    """   
    __PATTERN = re.compile('(\\d+)\\s*-\\s*(\\d+)\\s*-\\s*(\\d+)\\s*(\\d+)\\s*DESIGNS\\\\([a-zA-Z][^\\\\]*)$');
    def __init__(self, dirname):
        super().__init__(dirname)
    def __call__(self):
        match = ADFP4.__PATTERN.search(self.dirname)
        if match:
            self.date = date(int(match.group(1)),
                    int(match.group(2)), int(match.group(3)))
            self.title = match.group(5)
            return True
        return False
    def pattern(self):
        return "PATTERN4"
