"""
module : envogue

Creates artwork objects based on the organization of directories at envogue
design storage server.

"""
from os import path
import os
from datamodel.artwork import AArtwork
from datamodel.error import AError
from studio.updater import Updater
from common import fileutil
import re
from datetime import date


class DesignFactory(object):
    """ Creates artwork objects from a uri

    Each studio creates organizes their artwork in a specific format. This
    class constructs the artwork for a Artwork Design studio based on their
    organization at the specifc company.

    Attributes:
        repos : This is the repository containing all the artwork from this
                studio
        db    : This is a list in which the constructed artwork objects will
                be placed.
    """
    # NOTE : THIS IS WINDOWS SPECIFC - NEED TO MAKE IT PLATFORM INDEPENDENT
    DIR_PATTERN = re.compile(r"\\(\d{4})-(\d{2})-(\d{2})\s-\s([a-zA-Z][^\\]*)$")
    def __init__(self, repos, db):
        if path.exists(repos):
            self._repos = repos
        else:
            raise AError("Repository specified does not exist : " + self._repos)
        self._db = db
    
    def create(self):
        """ Creates artwork objects from folders.

        Each folder has some metadata associated with artwork encoded in them.
        This function iterates through all the folders and adds an artwork object
        only if the folder is conformant.
        """
        dirs = [path.join(self._repos,d) for d in os.listdir(self._repos) 
                if path.isdir(path.join(self._repos,d))]
        for d in dirs:
            match = DesignFactory.DIR_PATTERN.search(d)
            if match:
                sdirs = [path.join(d,s) for s in os.listdir(d) 
                        if path.isdir(path.join(d,s))]
                if len(sdirs) != 1:
                    print("Expected only one subdirectory in " + d)
                    continue
                date_created = date(int(match.group(1)),
                        int(match.group(2)), int(match.group(3)))
                name = match.group(4)
                studio = "Artwork Design"
                artwork = AArtwork(name, studio, date_created)
                artwork.uri = sdirs[0]
                artwork.original_name = path.basename(path.normpath(sdirs[0]))
                updater = Updater(artwork)
                updater.classifier_location = "C:\\Users\\asundararajan\\sources\\analytics\\designware\\python\\studio\\data"
                try:
                    updater.run()
                    self._db.append(artwork)
                except AError as err:
                    print("**** " + d + " has a problem ")
                    print(err.message)
            else:
                print(d + " is not appropriately named.")
