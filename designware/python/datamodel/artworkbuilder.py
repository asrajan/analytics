""" 
Filename : artworkbuilder.py

Builds and returns an artwork object.

"""

from .artwork import AArtwork
from .name import AEntityName
from .error import AError
from datetime import date

class AArtworkBuilder:
    """ Builds an artwork object based on information obtained

    Builds an Artwork from information that is progressive gathered.
    """
    def __init__(self):
        """ Constructs a Builder object

        This needs to be maintained in Sync with Artwork.
        """
        self.__artwork = None
        self.__title = []
        self.__studio = []
        self.__date_created = []
    def set_title(self, title):
        """ Sets the title field in the builder

        Args:
            title : A String representing the title
        """
        self.__title = title
    def set_studio(self, studio):
        """ Sets the studio of the Artwork 

        Args:
            studio : A String representing the studio name
        """
        self.__studio = studio

    def set_date_created(self, date_created):
        """ Sets the date created

        Args:
            date_created : A date object
        """
        self.__date_created = date_created

    def get_artwork(self):
        """ Creates an artwork object

        Basic metadata associated with an artwork object
        must be known before it can be created
        """
        if self.__artwork:
            return self.__artwork

        if self.__title and self.__studio and self.__date_created:
            studio = AEntityName(self.__studio)
            self.__artwork = AArtwork(self.__title, 
                    self.__studio, self.__date_created)
        else:
            raise AError("Artwork constructions needs title, studio and date")
        return self.__artwork

    def __check_artwork(self):
        """ Check if artwork object is legal

        Raises an exception if artwork object is not created
        """
        if not self.__artwork:
            raise AError("Artwork object not builder.")
