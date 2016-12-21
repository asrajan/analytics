'''
module : test_check_stores.py

This modules tests that stores have valid formats.
'''
# Python STandard Libraries
import unittest
from datetime import date
from os       import path

# Application Libraries
from ecom        import AStores
from ecom        import ACheckStores
from core        import AQuery
from core        import ATable
from core        import AWriteTable
from core        import AQueryEngine
from credentials import ACredentials
from mailer      import AMailer

class TestCheckStores(unittest.TestCase):
    """ Test that stores are valid in their format.

    For the B2B eCommerce integration to work consistently it is important
    to ensure that for every stock product we want to display on the 
    B2B ecommerce site has a UPC reference assigned to it.
    """
    def test_check_stores(self):
        # Construct a Query Engine Connected to the Envogue Blue Cherry 
        #Data Base
        creds = ACredentials('.bccreds')
        qengine = AQueryEngine(server='ENVOGUE-BCDB', 
            user = creds.login,
            password = creds.passwd,
            database = 'dataEVPR',
            port = 1433)
        # Create a predefined Query Object to check the status of the UPC
        # data
        query = AStores()
        # Run Query to get the results
        qengine.execute(query)
        # Run filter
        results = ACheckStores(query)
        results.filter()
        # Generate the table name
        table_name = path.join(self.get_test_dir(),
            'Quality-Stores' + str(date.today()) + '.xlsx')
        AWriteTable(results.table, table_name).execute()
        mail_results = AMailer('asrajan@gmail.com','.gmail','Stores Test Results',
        '''Hi Receiver,
        
        Please find attached to this email the results of stores testing.
        
        The email should contain an attached Excel sheet. Please view in Microsoft Excel only.
        ''')
        mail_results.attach(table_name)
        mail_results.fire()
        
    def get_test_dir(self):
        return path.dirname(__file__)        
        
        

if __name__ == '__main__':
    unittest.main()

