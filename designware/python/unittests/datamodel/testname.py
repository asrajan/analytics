""" This file implements the unit tests for name module """
import unittest
from datamodel.name import APersonName
from datamodel.error import AError

class TestPersonName(unittest.TestCase):
    def test_name_fail(self):
        """ Tests that an empty name raises an exception """
        fname = ""
        mname = ""
        lname = ""
        self.assertRaises(AError, lambda: APersonName(fname, mname, lname))
    def test_name_print(self):
        """ Creates a valid name and prints it correctly """
        fname = "Arvind"
        lname = "Sundararajan"
        mname = ""
        myname = APersonName(fname, mname, lname);
        self.assertEqual("Arvind Sundararajan", str(myname))

class TestEntityName(unittest.TestCase):
    """ This class implements the unit tests for EntityNames """
    def test_entity_name_fail(self):
        """ Tests that empty entity name raises an exception """
        self.assertRaises(AError, lambda: AEntityName(""))
    def test_entity_name_pass(self):
        """ Verifies that a legal name is okay """
        stratton = AEntityName("stratton")
        self.assertEqual(str(stratton), "stratton")

if __name__ == '__main__':
    unittest.main()


