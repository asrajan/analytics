"""
File : imagefile.py

This file implements a class called AImageFile. This represents an image file
with a URL and other basic information.
"""
from .error import AError
from os import path
from PIL import Image
from PIL import IptcImagePlugin
import exifread

class AImageFile:
    """ Represents an image file on disk.

    Represents an image file on disk with additionally meta data associated
    with the image file.

    Attributes:
        __uri : A url to the image file (or a file path)
        __filetype : Usually based on extension - tiff, jpg etc.
        __metadata : dictionary of metadata associated with the image file
    """
    def __init__(self, uri):
        """ Constructs an ImageFile object from the uri passed 
        
        Constructs and loadsmetada of the image file.

        Args :
            uri : A String representing a uri or the image file path
        Raises :
            AError if the image file does not exist.
        """
        if not path.exists(uri):
            raise AError("URI specified does not exist : " + uri)
        im = Image.open(uri)
        if not im:
            raise AError("URI specified is not a supported image format : " + 
                    uri)
