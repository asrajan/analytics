'''
module : check_upc

This module implements all the classes to extract data that
will sent to b2b.
'''
from core import AQuery

class ACheckUPC(AQuery):
    ''' A query for inventory information.

    Blue Cherry maintains the running aggregates in a table called ZZXSSUMH.
    This table maintains quantity exchanged during every transaction that is
    entered into blue cherry.

    For each transaction in BlueCherry an entry is created in this table that
    details the quantities exchanged.

    The various transaction types are
    CC = Customer Cancel
    CH = House Cancel
    SA = Stock Adjustment
    RT = Return
    R1 = Received Units
    R2 = Irregular Receipt
    OP = Tranaction created by a Sales Order that has been opened 
    IN = Invoice - An invoice transaction takes place when the order moves 
                   out of warehouse
    PK = Picked - A picked transaction takes place when logistics moves 
                  an open sales order to pick state
    WP = Production - A transaction is created when production order is 
                placed (Total WIP or Work in Progress)
    CM = Consumed
    RV = Linked Received Units
    RI = Linked Invoice Units
    RP = Linked Pick Units
    RO = Linked Open Units
    RS = Reserved
    DM = Demand Units(???)
    ST = Ship To Location
    NS = No Ship To
    US = Uncovered Demand

    The above table is available at - 
        http://bcwiki.bluecherry.com/bcwiki/index.php?title=Inventory_Inquiry

    The transaction type field in ZZXSSUMH is REC_TYPE. For some reason the
    quantity per transaction is always filled in SIZE02_QTY column of the
    table.

    Formula per SKU is
        QOH             = SA + RT + R1 + R2 - IN - CM + RV - RI
        OTS             = SA + RT + R1 + R2 - IN - CM - PK - RS - OP - DM
        OTS_SHIP_TO_WIP = SA + RT + R1 + R2 - IN - PK - OP - CM - RS - DM + ST + RV - RI - RP - RO 

    The query below performs the aggregation over the types of transaction described above.
    ZZXBUCKT is used to creating the sum by using cross product to split each of the quantities
    associated with a different type of tranaction using cross join.

    '''
    def __init__(self, ots = 50):
        self._ots = ots
        super().__init__()
        
    def _init_query(self):
        self._query = '''SELECT (s.style) AS Style_Number,
            (s.division) AS Division, 
            (ss.color_code) AS Color_Code, 
            (ss.dimension) AS Dimension,
            (ss.lbl_code) AS  Lbl_code, 
            (ss.Location) AS Location,
            ((IsNull(qfusa,0)+IsNull(qfurt,0)+IsNull(qfur1,0)+IsNull(qfur2,0)-IsNull(qfuin,0)-IsNull(qfucm,0))+(IsNull(qfurv,0)-IsNull(qfuri,0))) AS Total_QOH, 
            -- (ss.qfuop) AS Open__, 
            -- (ss.qfupk) AS Pick, 
            (IsNull(qfur1,0)+IsNull(qfur2,0)+IsNull(qfurt,0)+IsNull(qfusa,0)-IsNull(qfuin,0)-IsNull(qfucm,0)-IsNull(qfupk,0)-IsNull(qfurs,0)-IsNull(qfuop,0)-IsNull(qfudm,0)) AS OTS_INV, 
            -- ((IsNull(qfusa,0)+IsNull(qfurt,0)+IsNull(qfur1,0)+IsNull(qfur2,0)-IsNull(qfuin,0)-IsNull(qfupk,0)-IsNull(qfuop,0)-IsNull(qfucm,0)-IsNull(qfurs,0)-IsNull(qfudm,0))+IsNull(qfust,0)+(IsNull(qfurv,0)-IsNull(qfuri,0)-IsNull(qfurp,0)-IsNull(qfuro,0))) AS Total_OTS_Ship_To_WIP, 
            -- (ss.qfuin) AS Invoice, 
            -- (ss.size_bk) AS Size_Bk, 
            (U.UPC) AS UPC
            from (
                select d.division, 
                    d.style, 
                    d.color_code, 
                    d.lbl_code, 
                    d.dimension,
                    d.location,
                    d.lot, size_num AS Size_Bk, 
                    sum(case Rec_Type when 'CC' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFUCC,
                    sum(case Rec_Type when 'CH' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFUCH,
                    sum(case Rec_Type when 'CM' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFUCM,
                    sum(case Rec_Type when 'DM' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFUDM,
                    sum(case Rec_Type when 'IN' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFUIN,
                    sum(case Rec_Type when 'OP' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFUOP,
                    sum(case Rec_Type when 'PK' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFUPK,
                    sum(case Rec_Type when 'R1' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFUR1,
                    sum(case Rec_Type when 'R2' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFUR2,
                    sum(case Rec_Type when 'RI' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFURI,
                    sum(case Rec_Type when 'RO' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFURO,
                    sum(case Rec_Type when 'RP' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFURP,
                    sum(case Rec_Type when 'RS' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFURS,
                    sum(case Rec_Type when 'RT' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFURT,
                    sum(case Rec_Type when 'RV' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFURV,
                    sum(case Rec_Type when 'SA' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFUSA,
                    sum(case Rec_Type when 'ST' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFUST,
                    sum(case Rec_Type when 'WP' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFUWP,
                    sum(case Rec_Type when 'NW' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFUNW,
                    sum(case Rec_Type when 'NS' then  Size01_Qty*sz01+  Size02_Qty*sz02+  Size03_Qty*sz03+  Size04_Qty*sz04+  Size05_Qty*sz05+  Size06_Qty*sz06+  Size07_Qty*sz07+  Size08_Qty*sz08+  Size09_Qty*sz09+  Size10_Qty*sz10+  Size11_Qty*sz11+  Size12_Qty*sz12+  Size13_Qty*sz13+  Size14_Qty*sz14+  Size15_Qty*sz15+  Size16_Qty*sz16+  Size17_Qty*sz17+  Size18_Qty*sz18+  Size19_Qty*sz19+  Size20_Qty*sz20+  Size21_Qty*sz21+  Size22_Qty*sz22+  Size23_Qty*sz23+  Size24_Qty*sz24 else 0 end) as QFUNS
                FROM zzxssumh d
                CROSS JOIN ZZXBUCKT b
                JOIN ZZXSCOLR c 
                    ON c.style = d.style
                    AND c.color_code = d.color_code
                    AND c.lbl_code = d.lbl_code
                    AND c.dimension = d.dimension
                    AND c.division = d.division
                WHERE 
                    CASE SIZE_NUM  
                        WHEN 01 THEN Call01 
                        WHEN 02 THEN Call02 
                        WHEN 03 THEN Call03 
                        WHEN 04 THEN Call04 
                        WHEN 05 THEN Call05 
                        WHEN 06 THEN Call06 
                        WHEN 07 THEN Call07 
                        WHEN 08 THEN Call08 
                        WHEN 09 THEN Call09 
                        WHEN 10 THEN Call10 
                        WHEN 11 THEN Call11 
                        WHEN 12 THEN Call12 
                        WHEN 13 THEN Call13 
                        WHEN 14 THEN Call14 
                        WHEN 15 THEN Call15 
                        WHEN 16 THEN Call16 
                        WHEN 17 THEN Call17 
                        WHEN 18 THEN Call18 
                        WHEN 19 THEN Call19 
                        WHEN 20 THEN Call20 
                        WHEN 21 THEN Call21 
                        WHEN 22 THEN Call22 
                        WHEN 23 THEN Call23 
                        WHEN 24 THEN Call24 
                    END = 'Y'
                GROUP BY d.division, d.style, d.color_code, d.lbl_code, d.dimension, d.location, d.lot, size_num) ss
            LEFT JOIN zzxscolr c
            ON c.division = ss.division
                AND c.style = ss.style
                AND c.color_code = ss.color_code
                AND c.lbl_Code = ss.lbl_code
                AND c.dimension = ss.dimension
            LEFT JOIN zzxstylr s
            ON s.pkey = c.fkey
            LEFT JOIN ZZEUPCNR u
            ON c.Division = u.Division
                AND c.style = u.style
                AND c.color_code = u.color_code
                AND c.lbl_code = u.lbl_code
                AND c.dimension = u.dimension
            WHERE 
                CASE ss.Size_Bk  
                    WHEN 01 THEN Call01 
                    WHEN 02 THEN Call02 
                    WHEN 03 THEN Call03 
                    WHEN 04 THEN Call04 
                    WHEN 05 THEN Call05 
                    WHEN 06 THEN Call06 
                    WHEN 07 THEN Call07 
                    WHEN 08 THEN Call08
                    WHEN 09 THEN Call09 
                    WHEN 10 THEN Call10
                    WHEN 11 THEN Call11
                    WHEN 12 THEN Call12
                    WHEN 13 THEN Call13
                    WHEN 14 THEN Call14
                    WHEN 15 THEN Call15
                    WHEN 16 THEN Call16
                    WHEN 17 THEN Call17
                    WHEN 18 THEN Call18
                    WHEN 19 THEN Call19
                    WHEN 20 THEN Call20
                    WHEN 21 THEN Call21
                    WHEN 22 THEN Call22
                    WHEN 23 THEN Call23
                    WHEN 24 THEN Call24
                END = 'Y'
            AND 1=1 
            AND ((IsNull(QFUR1,0)+IsNull(QFUR2,0)+IsNull(QFURT,0)+IsNull(QFUSA,0)-IsNull(QFUIN,0)-IsNull(QFUCM,0)-IsNull(QFUPK,0)-IsNull(QFURS,0)-IsNull(QFUOP,0)-IsNull(QFUDM,0)) >= %s)
            AND (ss.location != 'FOB') AND (ss.location != '') AND (ss.location != 'POE')
            AND (u.upc IS NULL)
            ORDER BY s.style,
                s.division,
                ss.color_code,
                ss.dimension,
                ss.lbl_code
        '''
        self._query_tuple = (self._ots,)
