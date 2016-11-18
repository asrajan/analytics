""" This script goes through the existing archive of images and creates a 
list or artwork objects """
from datamodel.error import AError
import os
from os import path
class AArtworkListBuilder(object):
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
        if not path.exists(self.root_dir):
            raise AError(root_dir + " does not exist on system. Please check.")
        if not path.isdir(self.root_dir):
            raise AError(self.root_dir + " is not a folder/directory.")
        self.__walk()
        
    def __walk(self):
        """ Walks the directory tree and prints all the sub directories and 
        files
        """
        self.__dir_tree = os.walk(self.root_dir)
