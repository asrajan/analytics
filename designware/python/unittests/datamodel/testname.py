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

if __name__ == '__main__':
    unittest.main()


