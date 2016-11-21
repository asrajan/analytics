""" This file implements the unit tests for imagefile module """
import unittest
from datamodel.imagefile import AImageFile 
from datamodel.error import AError
import os

class TestImageFile(unittest.TestCase):
    def test_valid_construction(self):
        """ This test verifies that an AImageFile object can be created """
        tif_file = ""
        for root,dirs,files in os.walk("."):
            for file in files:
                print(file)
                name,ext = os.path.splitext(file)
                if ext.lower() == ".tif":
                    tif_file = file
                    break
            break
        im = AImageFile(tif_file)

if __name__ == '__main__':
    unittest.main()
