from envogue.artworkasset import ArtworkAsset
import unittest
class TestArtworkAsset(unittest.TestCase):
    """ This class tests that artwork asset data is consistent """
    def test_artwork_asset(self):
        assets = ArtworkAsset()
        #print(assets.search('FPRINT1723CFIN', 'Artwork Design'))
        print(assets.cost('AW47956', 'Artwork Design'))
        

if __name__ == '__main__':
    unittest.main()
