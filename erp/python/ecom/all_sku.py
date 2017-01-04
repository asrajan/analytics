''' 
module : all_sku

Creates a query that returns all the Active SKUs from the and the properties
of the active SKU that make up a SKU. In addition UPC is also included.
'''


from core import AQuery

class AAllSKU(AQuery):
    ''' A query that constructs a list of all SKUs along with its UPC.
    
    '''
    def __init__(self):
        super().__init__()
    
    def _init_query(self):
        self._query = '''SELECT (s.style) AS Style_Number,
            (c.division) AS Division, 
            (c.color_code) AS Color_Code, 
            (c.dimension) AS Dimension,
            (c.lbl_code) AS  Lbl_code,
            (u.upc) AS UPC
        FROM zzxstylr s
        JOIN zzxscolr c
        ON (s.pkey = c.fkey)
        LEFT JOIN zzeupcnr u
        ON c.Division = u.Division
            AND c.style = u.style
            AND c.color_code = u.color_code
            AND c.lbl_code = u.lbl_code
            AND c.dimension = u.dimension
        WHERE s.active_ok = 'Y'
        '''
        self._query_tuple = ()

class AAllSKUImages(AQuery):
    ''' All SKUs and the associated image files '''
    def __init__(self):
        super().__init__()
    
    def _init_query(self):
        self._query = '''SELECT (s.style) AS Style_Number,
            (c.division) AS Division, 
            (c.color_code) AS Color_Code, 
            (c.dimension) AS Dimension,
            (c.lbl_code) AS  Lbl_code,
            (img.stor_file) AS Color_Image,
            (imgh.stor_file) AS Style_Image
        FROM zzxstylr s
        LEFT JOIN zzxscolr c
        ON (s.pkey = c.fkey)
        LEFT JOIN zvstimgp img
        ON img.division = c.division
            AND img.style = c.style
            AND img.color_code = c.color_code
            AND img.lbl_code = c.lbl_Code
            AND img.dimension = c.dimension
            AND img.prime_image = 'Y'
            AND img.contextid = 'ZZXSCOLR'
        LEFT JOIN zvstimgp imgh
        ON imgh.division = c.division
            AND imgh.style = c.style
            AND imgh.prime_image = 'Y'
            AND imgh.contextid = 'ZZXSTYLR'
        WHERE (img.stor_file LIKE '%.tif')
            OR (img.stor_file LIKE '%.tiff')
            OR (img.stor_file LIKE '%.TIF')
            OR (img.stor_file LIKE '%.TIFF')
            OR (imgh.stor_file LIKE '%.tif')
            OR (imgh.stor_file LIKE '%.tiff')
            OR (imgh.stor_file LIKE '%.TIF')
            OR (imgh.stor_file LIKE '%.TIFF')
        '''
        self._query_tuple = ()


    
