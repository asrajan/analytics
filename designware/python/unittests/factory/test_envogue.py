from envogue.artworkasset import ArtworkAsset
from datamodel.artwork import APattern 
from datamodel.artwork import AArtwork 
from datamodel.error import AError
from datetime import date
from factory.envogue import DesignFactory
import unittest

class TestDesignFactory(unittest.TestCase):
    """ This class collects the ArtworkDesign Factory class """
    def test_design_factory(self):
        print("Reached Here")
        repos = "M:\\Design Studios\\Artwork Design"
        db = list()
        factory = DesignFactory(repos, db)
        factory.create()
        dba = ArtworkAsset()
        for entry in db:
            print(entry.name)
            cost = dba.cost(entry.original_name, "Artwork Design")
            if cost:
                print(cost)
            

if __name__ == '__main__':
    unittest.main()
