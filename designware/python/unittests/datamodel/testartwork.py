""" This file implements the unit tests for artwork module """
import unittest
from datamodel.artwork import APattern 
from datamodel.artwork import AArtwork 
from datamodel.error import AError
from datetime import date

class TestPattern(unittest.TestCase):
    """ This class tests the APattern class """
    def test_pattern_fail(self):
        """ Tests that incorrect pattern specification causes failure """
        self.assertRaises(AError, lambda: APattern("junk"))
    def test_pattern_pass(self):
        """ Tests that correct pattern can be constructed """
        pattern = APattern("floral")
        self.assertTrue(pattern.index())
    def test_empty_pattern(self):
        """ Tests that a pattern can be initialized as empty """
        empty_pattern = APattern("")
        self.assertFalse(empty_pattern)

class TestArtwork(unittest.TestCase):
    """ This class tests the Artwork base class """
    def test_create_artwork(self):
        date_created = date.today()
        title = "MonaLisa"
        studio = "Gogh Artworks"
        artwork = AArtwork(title, studio, date_created)
        if not artwork.get_designer():
            artwork.set_designer("Vincent", "Van", "Gogh")
        self.assertTrue(artwork.get_designer())




if __name__ == '__main__':
    unittest.main()
