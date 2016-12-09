"""

module : queries

This module defines miscellaneous classes of queries generally useful
in inventory management

"""
from query import AQuery

class AAllSKU(AQuery):
    """ Defines a query to return All SKUs 

    Execution of this query returns all the SKUs contained in the database.

    Note : This includes inactive SKUs as well.
    """
    def __init__(self):
        super().__init__()

    def _init_query(self):
        self._query = '''SELECT zzxstylr.style as Style_Number, 
            zzxscolr.division as Division,
            zzxscolr.color_code as Color,  
            zzxscolr.lbl_code as Label,  
            zzxscolr.dimension as Dimension 
        FROM zzxstylr join zzxscolr 
        ON (zzxstylr.pkey = zzxscolr.fkey)
        ORDER BY zzxstylr.style,
            zzxscolr.division,
            zzxscolr.color_code,  
            zzxscolr.lbl_code,  
            zzxscolr.dimension
        '''
        self._query_tuple = ()

class AActiveSKU(AQuery):
    """ Defines a query to return All SKUs 

    Execution of this query returns all the Active SKUs contained in 
    the database.
    """
    def __init__(self):
        super().__init__()

    def _init_query(self):
        self._query = '''SELECT zzxstylr.style as Style_Number, 
            zzxscolr.division as Division,
            zzxscolr.color_code as Color,  
            zzxscolr.lbl_code as Label,  
            zzxscolr.dimension as Dimension 
        FROM zzxstylr join zzxscolr 
        ON (zzxstylr.pkey = zzxscolr.fkey)
        WHERE (zzxstylr.active_ok = 'Y')
        ORDER BY zzxstylr.style,
            zzxscolr.division,
            zzxscolr.color_code,  
            zzxscolr.lbl_code,  
            zzxscolr.dimension
        '''
        self._query_tuple = ()


class AActiveUPC(AQuery):
    """ Returns a table of active SKUs and the associated UPC 
    
    UPC is a unique number assigned to each SKU. This number must be assigned
    to enable trabsactions using EDI.
    """
    def __init__(self):
        super().__init__()
    def _init_query(self):
        self._query = '''SELECT zzxstylr.style AS Style_Number,
            zzxscolr.division AS Division,
            zzxscolr.color_code AS Color_Code,
            zzxscolr.lbl_code AS Lbl_Code,  
            zzxscolr.dimension AS Dimension,
            zzeupcnr.upc AS UPC
        FROM zzxstylr JOIN 
            (zzxscolr LEFT JOIN zzeupcnr
                ON (ZZXSCOLR.style = ZZEUPCNR.style) 
                and (ZZXSCOLR.division = ZZEUPCNR.division) 
                and (ZZXSCOLR.color_code = ZZEUPCNR.color_code) 
                and (ZZXSCOLR.lbl_code = ZZEUPCNR.lbl_code) 
                and (ZZXSCOLR.dimension = ZZEUPCNR.dimension))
        ON (zzxstylr.pkey = zzxscolr.fkey)
        WHERE (zzxstylr.active_ok = 'Y')'''
        self._query_tuple = ()


class AReceivedStock(AQuery):
    """ Defines a query to understand what items have been received

    This is a query to obtain all of the quantities of styles that have been
    received so far.
    """
    def __init__(self):
        super().__init__()

    def _init_query(self):
        self._query = '''SELECT zzcordrd.style AS Style_Number, 
            zzcordrd.division AS Division,
            zzcordrd.color_code AS Color,
            zzcordrd.lbl_code AS Label,
            zzcordrd.dimension AS Dimension,
            zzcordrd.location AS Location,
            SUM(ZZCORDRD.total_qty) AS Total
        FROM zzcordrd
        WHERE (zzcordrd.stage = 'recv') 
            and (zzcordrd.location != 'POE')
            and (zzcordrd.location != 'FOB')
            and (zzcordrd.location != '')
        GROUP BY zzcordrd.style,
            zzcordrd.division,
            zzcordrd.color_code, 
            zzcordrd.lbl_code,
            zzcordrd.dimension,
            zzcordrd.location'''
        self._query_tuple = ()

class AStockSales(AQuery):
    """ Creates a query that returns all the stock sales
    """
    def __init__(self):
        super().__init__()
    def _init_query(self):
        self._query = '''SELECT zzoordrd.ord_num as Order_Number,
            zzoordrh.ord_status AS Status,
            zzoordrd.style AS Style_Number,
            zzoordrd.division AS Division,
            zzoordrd.color_code AS Color,
            zzoordrd.lbl_code AS Label,
            zzoordrd.dimension AS Dimension,
            zzoordrd.location AS Location,
            zzoordrh.customer AS Customer,
            zzoordrd.total_qty AS Quantity
        FROM zzoordrd JOIN zzoordrh 
        ON (zzoordrd.fkey = zzoordrh.pkey)
        WHERE (zzoordrd.Location != 'POE')
            and (zzoordrd.LOCATION !='FOB')
            and (zzoordrd.LOCATION != '')'''
        self._query_tuple = ()

class AStockCustomers(AQuery):
    """ Creates a query that returns all the customers of stock
    sales
    """
    def __init__(self):
        super().__init__()
    def _init_query(self):
        self._query = '''
        SELECT DISTINCT zzoordrh.customer as Customer,
            zzoordrh.Department as Department
        FROM zzoordrd JOIN zzoordrh 
        ON (zzoordrd.fkey = zzoordrh.pkey)
        ORDER BY zzoordrh.customer'''
        self._query_tuple = ()




