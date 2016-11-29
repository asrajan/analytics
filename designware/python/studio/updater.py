"""
module : updater

Updates an artwork with information derived from files supplied by studio

TODO : Currently, this folder also has Envogue specific information that 
we MUST refactor out. The envoge specific information are the INDEX files and
possibly FLAT files that are created by Envogue designers.

"""
# Imports from repository
from datamodel.error import AError
from datamodel.artwork import AArtwork
from common import fileutil
# imports from python library
import re
import json
import os
from os import path

class Updater(object):
    """ Extracts information from a folder supplied by the studio and
    updates attributes of the artwork object. 

    Each studio supplies artwork in the form of files representing the
    design. Each of these files have a specific function. This class
    mines the directory and extracts all relevant information to 
    describe the set of files present in the folder.

    Attributes:
        _artwork : Reference to the data base artwork object - this must
        contain information about which studio it belongs to. It must also
        contain the uri or the folder path containing the artwork as 
        produced by the studio.
        _classifier : This is a meta data that is used for classification
        of the files for the artwork studio.
    """
    CHECK_FORMAT = {# Callbacks for checking format of the file
        "layer":"_layer", 
        "index":"_index", 
        "full":"_full", 
        "texture":"_texture", 
        "flat":"_flat"}

    ADD_FILE = {#Call backs for updating the artwork object with file info
        "layer":"_add_layer", 
        "index":"_add_index", 
        "full":"_add_full", 
        "texture":"_add_texture", 
        "flat":"_add_flat"}

    def __init__(self, artwork):
        """ Constructs the artwork builder object for ArtworkDesign

        Args:
            __artwork : A reference to an artwork object
            _classifier : A files classifier object
            _classifier_location : Folder containing the classifiers

        """
        if str(artwork.studio) == self.name():
            self._artwork = artwork
        else:
            raise AError("This artwork is not for " + self.name())
        self._classifier = None
        self._classifier_location = None 
    
    @property
    def classifier_location(self):
        return self._classifier_location
    
    @classifier_location.setter
    def classifier_location(self, classifier_location):
        """ Sets the classifier location.

        Args:
            classifier_location : A uri of a filesystem path
        Raises:
            AError if the folder/path/uri does not exist
        """
        if not path.exists(classifier_location):
            raise AError(classifier_location + " is not a valid path")
        self._classifier_location = classifier_location

    def _load_classifier(self):
        """ Based on the studio initializes the classifier object.

        This method loads the classifier meta data that is used by the
        file classification engine.

        Pre-requisites:
            classifier_location must be set
        """
        if not self.classifier_location:
            raise AError("Classifier location must be set prior to call")
        classifier_file = path.join(self.classifier_location, 
                self._classifier_name_from_studio_name(str(self._artwork.studio)))
        # Wrap the next two calls with try catch and transfrom
        # to AError
        fp = open(classifier_file, "r")
        self._classifier = json.load(fp)
        fp.close()
        return

    def _classifier_name_from_studio_name(self, name):
        """ Returns the classifier name from the studio name """
        name = (re.sub("\\s+","_", name)).lower() + ".json"
        return name

    def run(self):
        """ Checks and populates that artwork object from an image folder 

        Checks to see if the folder containing artwork images is conformant and
        populates the artwork object with meta data
        """
        self._load_classifier()
        self._run(False)
    
    def _run(self, check_only = True):
        """ Goes through each element in the artwork directory and ensures that
        the format of the files is as expected.
        """
        for root,dirs,files in os.walk(self.artwork.uri):
            if len(dirs) > 0:
                raise AError("Detected unrecognized subdirectories")
            for file in files:
                if fileutil.is_hidden_file(file):
                    continue
                if not fileutil.is_tiff(file):
                    raise AError("Unrecognized file detected : " + file)
                base,ext = path.splitext(file)
                if self._ignore(base):
                    continue
                search_order = self._classifier["formats"]["search_order"]
                file_classified = False 
                for file_type in search_order:
                    method_name = Updater.CHECK_FORMAT[file_type]
                    dispatch = type(self).__dict__[method_name].__get__(self, type(self))
                    if dispatch(base):
                        file_classified = True
                        if not check_only:
                            method_name = Updater.ADD_FILE[file_type]
                            dispatch = type(self).__dict__[method_name].__get__(self, type(self))
                            dispatch(file)
                        break
                if file_classified:
                    continue
                raise AError("Unrecognized file " + file)
        return True

    def _check_file_pattern(self, file, plist):
        """ Checks if the file basename matches a pattern from a list of patterns """
        for file_format in plist:
            if re.compile(file_format).search(file):
                return True
        return False

    def _ignore(self,file):
        """ Returns true if the file must be ignored """
        return self._check_file_pattern(file, self._classifier["formats"]["ignore_files"])
    
    def _layer(self,file):
        """ Returns true if the file must be ignored """
        return self._check_file_pattern(file, self._classifier["formats"]["layer"])
    def _index(self,file):
        """ Returns true if the file must be ignored """
        return self._check_file_pattern(file, self._classifier["formats"]["index"])
    def _texture(self,file):
        """ Returns true if the file must be ignored """
        return self._check_file_pattern(file, self._classifier["formats"]["texture"])
    def _flat(self,file):
        """ Returns true if the file must be ignored """
        return self._check_file_pattern(file, self._classifier["formats"]["flat"])
    def _full(self,file):
        """ Returns true if the file must be ignored """
        return self._check_file_pattern(file, self._classifier["formats"]["full"])
    
    def _add_layer(self,file):
        """ Adds the file to the artwork object """
        self._artwork.append_layer_file(file)
    def _add_index(self,file):
        """ Adds the file to the artwork object """
        self._artwork.append_layer_file(file)
    def _add_full(self,file):
        """ Adds the file to the artwork object """
        self._artwork.full_file = file
    def _add_texture(self,file):
        pass
    def _add_flat(self,file):
        """ Returns true if the file must be ignored """
        self._artwork.flat_file = file

    def name(self):
        return "Artwork Design"

    @property
    def artwork(self):
        return self._artwork

    @artwork.setter
    def artwork(self, artwork):
        self._artwork = artwork
