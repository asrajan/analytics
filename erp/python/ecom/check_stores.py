'''
module: check_stores

Checks that store names and addresses are clean

'''
# Imports from standard library
import re
from   copy import copy

#imports from the application library
from   core import AQuery
from   core import AQueryError
from   core import AFilter
from   core import ATable

class AStores(AQuery):
    ''' A query to check if the store information in BlueCherry is clean.
    
    A number of store information have been entered into blue cherry. These
    stores need to be imported into the eCommerce site. The store name, store
    and address information should all be valid.
    
    '''
    def __init__(self):
        super().__init__()
    
    def _init_query(self):
        self._query = '''
        SELECT  zzxstorr.pkey pkey,           -- 0
            zzxstorr.CUSTOMER CUSTOMER,       -- 1
            zzxstorr.ACTIVE_OK ACTIVE_OK,     -- 2
            zzxstorr.STORE_NAME STORE_NAME,   -- 3
            zzxstorr.STORE STORE,             -- 4
            zzxstorr.EDI_STORE EDI_STORE,     -- 5
            zzxstorr.OLD_STORE OLD_STORE,     -- 6
            zzxstorr.ADDRESS1 ADDRESS_LINE1,  -- 7
            zzxstorr.ADDRESS2 ADDRESS_LINE2,  -- 8
            zzxstorr.ADDRESS3 ADDRESS_LINE3,  -- 9
            zzxstorr.ADDRESS4 ADDRESS_LINE4,  -- 10
            zzxstorr.CITY CITY,               -- 11
            zzxstorr.STATE STATE1,            -- 12
            zzxstorr.ZIPCODE ZIPCODE,         -- 13
            zzxstorr.COUNTRY COUNTRY          -- 14
        FROM zzxstorr
        WHERE (zzxstorr.active_ok = 'Y')
        ORDER BY zzxstorr.store
        '''
        self._query_tuple = ()
 
class ACheckStores(AFilter):
    ''' Filters only invalid customer stores '''
    _CHECKERS = {#Call backs for updating the artwork object with file info
        "_check_address", 
        "_check_zip_code", 
        "_check_country", 
        "_check_state", 
        "_check_store"}
        
    def __init__(self, query):
        super().__init__(query,True)
    
    def _filter(self):
        ''' Implements a filter that locates invaid addresses and 
        uses them for error correction.
        '''
        self._table._data = []
        for entry in self._query._table._data:
            for checker in ACheckStores._CHECKERS:
                dispatch = type(self).__dict__[checker].__get__(self, type(self))
                res,reason = dispatch(entry)
                if res:
                    new_entry = copy(entry)
                    new_entry.append(reason)
                    self._table._data.append(new_entry)
                    break
    
    def _check_address(self, entry):
        ''' Checks that atleast one of the address lines is not empty '''
        address_line1 = entry[7]
        address_line2 = entry[8]
        address_line3 = entry[9]
        address_line4 = entry[10]
        if ((not address_line1) and 
            (not address_line2) and
            (not address_line3) and
            (not address_line4)):
            return (True, 'All address lines are empty')
        return (False, '')
    
    def _check_zip_code(self, entry):
        if not entry[13]:
            return (True, 'Zip Code is not Specified')
        return (False, '')
            
    def _check_state(self, entry):
        if not entry[12]:
            return (True, 'State is not specified')
        return (False, '')
    
    def _check_country(self, entry):
        if not entry[14]:
            return (True, 'Country is not specified')
        return (False, '')
    
    def _check_store(self, entry):
        ''' Checks that the store names are conformant '''
        #if (not (entry[4] == entry[5])):
        #    return (True, 'EDI Store does not match Store')
        STORE = re.compile(r'[a-zA-Z0-9]+')
        if not re.fullmatch(STORE,entry[4]):
            return (True, 'Store name should ONLY include Alpha-Numerics')
        return (False, '')
        
            
        
    
    
    
        



