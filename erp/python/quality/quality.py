'''
module : quality.py

This file contains the scripts to fire UPC quality. UPC code is required
for each item that is displayed on the ecommerce site to enabling ordering 
of items from the eCommerce site.
'''
# Python STandard Libraries
from datetime    import date
from os          import path
from os          import remove

# Application Libraries
from ecom        import AAllEComStock
from ecom        import ACheckUPC

from ecom        import AAllSKU
from ecom        import AAllSKUImages
from ecom        import ACheckImages
from ecom        import ACheckUPCFilter

from core        import AQuery
from core        import ATable
from core        import AWriteTable
from core        import AQueryEngine
from credentials import ACredentials
from mailer      import AMailer

def target_dir():
    return path.dirname(__file__) 


class AEComQualityMonitor:
    ''' Monitors the quality of data for eCommerce deployment.
    
    ECommerce deployment requires certain rules in the data. Examples of these
    rules include assignment of valid UPC as well as images to relevant styles.
    This class monitors the health of the data and fires emails to the stake
    holders.
    
    Attributes:
        _qengine : Connects to the relevant data base
    '''
    def __init__(self):
        self._qengine = None
        self._attachments = []
        self._init_qengine()
        self._init_n_skus()
    
    def _init_qengine(self):
        creds = ACredentials('.bccreds')
        self._qengine = AQueryEngine(server='ENVOGUE-BCDB', 
            user = creds.login,
            password = creds.passwd,
            database = 'dataEVPR',
            port = 1433)
    
    def _init_n_skus(self):
        all_ecom_stock_query = AAllEComStock()
        self._qengine.execute(all_ecom_stock_query)
        self._n_skus = len(all_ecom_stock_query)
    
    def _collect_upc_quality(self):
        q_all_skus = AAllSKU()
        self._qengine.execute(q_all_skus)
        q_upc = ACheckUPC()
        self._qengine.execute(q_upc)
        q_upc = ACheckUPCFilter(q_upc, q_all_skus)
        q_upc.filter()
        self._n_wo_upc = len(q_upc)     
        ss_upc = path.join(target_dir(),
            'UPC-Quality-' + str(date.today()) + '.xlsx')        
        AWriteTable(q_upc.table, ss_upc).execute()
        self._attachments.append(ss_upc)
    
    def _collect_image_quality(self):
        q_images = ACheckImages()
        self._qengine.execute(q_images)
        self._n_wo_images = len(q_images)
        ss_images = path.join(target_dir(),
            'Images-Quality-' + str(date.today()) + '.xlsx')
        AWriteTable(q_images.table, ss_images).execute()
        self._attachments.append(ss_images)
    
    def _collect_quality(self):
        self._collect_image_quality()
        self._collect_upc_quality()
    
    def _send_email(self):
         # Formatted Results message
        t_message = '''     
        ECommerce Data Quality
        ======================
        
        This report contains data quality information for successful
        deployment of B2B ECommerce Site at Envogue International.
        
        UPC-Quality :
            Total SKUs for ECom - {:d}
            Total SKUs without UPC - {:d}
            Quality - {:.2f}%
        
        Images-Quality :
            Total SKUs for ECom - {:d}
            Total SKUs without Images - {:d}
            Quality - {:.2f}%
            
        More details on each of the tables can be found in the attached spread 
        sheets of the same name. Please note, the spread sheets should be 
        downloaded and opened using Microsoft Excel. Opening the spread sheets
        using Google Viewer or OpenOffice will not display the data correctly.
    
        - Team Ahana
        
        Note : This is an automated email. Please do not reply to the mail. For
        questions contact asrajan@gmail.com        
        '''
        message = t_message.format(self._n_skus, self._n_wo_upc, 
            (self._n_skus - self._n_wo_upc)/self._n_skus * 100,
            self._n_skus, self._n_wo_images, 
            (self._n_skus - self._n_wo_images)/self._n_skus * 100)
        mail_results = AMailer('.gmail',
            'Envogue ECommerce Quality',
            message
            )
        mail_results.add_recepient('asrajan@gmail.com',
            'INTERNAL_CUSTOMER',
            'Arvind',
            'Sundararajan'
            )
        mail_results.add_recepient('asrajan547@gmail.com',
            'INTERNAL_CUSTOMER',
            'Arvind',
            '',
            'Sundararajan'
            )
        mail_results.add_recepient('sheetal.naik@envogueinternational.com',
            'INTERNAL_CUSTOMER',
            'Sheetal',
            '',
            'Naik'
            )
        mail_results.add_recepient('sanket.kodolikar@envogueinternational.com',
            'INTERNAL_CUSTOMER',
            'Sanket',
            '',
            'Kodolikar'
            )
        mail_results.add_recepient('manoj.chirania@envogueinternational.com',
            'INTERNAL_CUSTOMER',
            'Manoj',
            '',
            'Chirania'
            )            
        for attachment in self._attachments:
            mail_results.attach(attachment)
        mail_results.fire()
   
    def _clean(self):
        for attachment in self._attachments:
            remove(attachment)
    
    def run(self):
        self._collect_quality()
        self._send_email() 
        self._clean()

def main():
    mon = AEComQualityMonitor()
    mon.run()
    
    
    
if __name__ == '__main__':
    main()

    