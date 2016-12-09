"""
module: test_check_upc.py

An integartion test that tests AQuery, ATable and AWriteTable in
checking that a particular non-empty UPC exists for a product stock.
"""
# Python STandard Libraries
import unittest
from datetime import date

# Application Libraries
from ecom import ACheckUPC
from core import AQuery
from core import ATable
from core import AWriteTable
from core import AQueryEngine
from core import AQueryCredentials


class TestCheckUPCQuality(unittest.TestCase):
    """ Tests the UPC Quality in the data set.

    For the B2B eCommerce integration to work consistently it is important
    to ensure that for every stock product we want to display on the 
    B2B ecommerce site has a UPC reference assigned to it.
    """
    def test_upc_quality(self):
        # Construct a Query Engine Connected to the Envogue Blue Cherry 
        #Data Base
        creds = AQueryCredentials()
        qengine = AQueryEngine(server='ENVOGUE-BCDB', 
            user = creds.login,
            password = creds.passwd,
            database = 'dataEVPR',
            port = 1433)
        # Create a predefined Query Object to check the status of the UPC
        # data
        query = ACheckUPC()
        # Run Query to get the results
        qengine.execute(query)
        # Generate the table name
        table_name = 'Quality-UPC' + str(date.today()) + ".xlsx"
        AWriteTable(query.table, table_name).execute()
        
        

if __name__ == '__main__':
    unittest.main()
		
		
