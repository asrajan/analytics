"""
Filename : testartworkbuilder.py

This file unit tests the artwork builder class
"""
import unittest
from datamodel.error import AError
from datamodel.artworkbuilder import AArtworkBuilder
from datamodel.artwork import AArtwork
from datetime import date


class TestArtworkBuilder(unittest.TestCase):
    def test_artwork_construction_failure(self):
        builder = AArtworkBuilder();
        with self.assertRaises(AError):
            builder.get_artwork()
    def test_artwork_construction_success(self):
        builder = AArtworkBuilder()
        studio = "Artwork Design"
        date_created = date.today()
        title = "bloom field"
        builder.set_studio(studio)
        builder.set_title(title)
        builder.set_date_created(date_created)
        self.assertTrue(builder.get_artwork())


if __name__ == '__main__':
    unittest.main()

