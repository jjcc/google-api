# -*- coding: utf-8 -*-
from io import StringIO
import sqlite3
import sys
from typing import Set

from cn_swindex import draw_chart_by_db
from cn_swindex import draw_candle_mpf
import requests
import pandas as pd
import datetime
import time
#from datetime import datetime,timedelta

token1=""
with open("tiingo.token") as f:
    token1 = f.readline()

sector_etfs = {"XLC","XLP","XLY","XLE","XLF","XLV","XLI","XLB","XLRE","XLK","XLU","XLSR"}
twenty1_century_etfs = {"KOMP","SIMS","HAIL","FITE","ROKT","CNRG"}

industry_etfs = {"KBE","KRE","KCE","KIE","XAR","XTN","XBI","XPH","XHE","XHS",
                 "XOP","XES","XME","XRT","XHB","XSD","XSW","XNTK","XITK","XTL","XWEB"}

smartbeta_etfs = {"SPYD","SDY","WDIV","DWX","EDIV","QUS","QWLD","QEFA","QEMM","ONEY",
                  "ONEV","ONEO","LGLV","SMLV","MMTM","VLU","DWFI"}

ishare_sector1_etf = {"IBB","IHI","IYW","IGV","IXN","SOXX","IGF","ITA","IGM","IYH","IXJ","ITB","IYG","IYF","IXC","IYC",
                      "IHF","IYJ","IYT","IDU","EUFN","IYK","KXI","RING","IYE","IGE","MXI","IYZ","IHE","IYM","IXP"}

ishare_sector2_etf = {"PICK","IEO","RXI","IXG","SLVP","WOOD","IAT","EXI","IDNA","JXI","IEZ","IHAK","IAI","IETC","IAK",
                      "FILL","IGN","VEGI","IEIH","IFRA","IEDI","IEHS","EMIF","IEME","IECS","IEFN"}

def get_quote_info(symbol, start_date, end_date, file_name = None ):
    """
    get quote info from data provider
    :param symbol:
    :param start_date:
    :param end_date:
    :param file_name:
    :return:
    """

    url = "https://api.tiingo.com/tiingo/daily/{}/prices?startDate={}&endDate={}&format=csv&token={}".format(symbol,
                                                                                                             start_date,
                                                                                                             end_date,
                                                                                                             token1)
    print(url)
    r = requests.get(url, timeout=10)
    rows = r.text.split("\n")[1:-1]
    CSV_DATA = StringIO(r.text)
    df = pd.read_csv(CSV_DATA)
    #df = pd.DataFrame(rows)
    #df = df.iloc[:, 0].str.split(",", 13, expand=True)
    df["Symbol"] = symbol
    #data1.append(df)
    #
    #df_final = pd.concat(data1)
    #df_final.drop(df_final.iloc[:, 6:13], axis=1, inplace=True)
    df_final = df
    if file_name is not None:
        df_final.to_csv(file_name, index=False)

    return df_final

def draw_chart_by_db(code, name, file, connection=None, days=89):
    if connection is None:
        conn = sqlite3.connect('sw_index.db')
    else:
        conn = connection
    c = conn.cursor()

    SQL_Query = pd.read_sql_query(
        f'select *  from daily_tick where Symbol = \'{code}\'   ORDER BY date(date) DESC limit {days}', conn)
    df0 = pd.DataFrame(SQL_Query)
    df = df0.iloc[::-1, :]  # reverse the sequence

    today = str(datetime.date.today())

    title = f'{name}:{today}'
    # old_cols = df.columns
    # new_cols = [c if c != "vol" else "volume" for c in old_cols]
    # df.columns = new_cols
    dfsub = df  # df.iloc[50:, :]
    sz = (8.0, 5.75)
    draw_candle_mpf(dfsub, title, file,fsize = sz)

def df_to_db(connection, df):
    """
    insert data frame into db
    :param conn:
    :param df:
    :return:
    """
    if len(df) == 0:
        return
    today = datetime.datetime.today()
    if connection is None:
        conn = sqlite3.connect('etf.db')
    else:
        conn = connection
    c = conn.cursor()
    for index, row in df.iterrows():
        c.execute(
            """INSERT INTO daily_tick([date], [open],[high],[low],[close],
            [volume],[adjOpen],[adjLow],[adjHigh],[adjClose],[adjVolume],[divCash],[splitFactor],[Symbol])
            values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)

            """,
            (row['date'], row['open'], row['high'], row['low'], row['close'],
             row['volume'], row['adjOpen'], row['adjLow'], row['adjHigh'], row['adjClose'], row['adjVolume'],
             row['divCash'], row['splitFactor'], row['Symbol']))
    c.close()

def harvest_missing(symbol_list, connection=None):
    """
    filling the missing data into db
    :return: dataframe of missing data in db
    """
    today = datetime.datetime.today()
    if connection is None:
        conn = sqlite3.connect('etf.db')
    else:
        conn = connection

    c = conn.cursor()
    a_symbol = next(iter(symbol_list))
    query = "SELECT max(date(date)) as latest FROM daily_tick WHERE Symbol = '%s' ;" % a_symbol
    c.execute(query)
    latest_str = c.fetchone()[0]

    # print(latest_str)
    latest_date = datetime.datetime.strptime(latest_str, "%Y-%m-%d")
    latest_date_next = latest_date + datetime.timedelta(days=1)
    latest_str_next = datetime.datetime.strftime(latest_date_next, "%Y-%m-%d")
    # print(leatest_str_next)

    today = datetime.datetime.today()
    end = today + datetime.timedelta(days=1)
    if latest_str_next == str(end.date()):
        return None

    harvest(symbol_list,conn,latest_str_next)

    # # start = latest
    # df = harvest_daily_info(list_file,
    #                         start_data=leatest_str_next,
    #                         end_date=str(end.date()),
    #                         sleeptime=0.5) #,

def harvest(symbol_list, connection, start_date, end_date = None):

    conn = connection
    if end_date ==  None:
        today = datetime.datetime.today()
        end = today + datetime.timedelta(days=1)
        end_str = str(end)
    else:
        end_str = end_date

    for s in symbol_list:
        df = get_quote_info(s,start_date,end_str)
        l = len(df)
        print(f'symbol:{s}, lenght:{l}')
        df_to_db(conn,df)


def test_get_sectors():
    start_date = '2019-06-03'
    end_date = str(datetime.now().date() - datetime.timedelta(days=1))

    #fn = r"data/historicalMSFT_quotes2.csv"
    for s in sector_etfs:
        fn = f"data/{s}_{end_date}.csv"
        get_quote_info(s, start_date,end_date,fn)

def test_draw_charts():
    #for s in sector_etfs:
    s = 'XLB'
    fn = f"data/{s}_2020-08-18.csv"
    df = pd.read_csv(fn)
    size0 = (8.0, 5.75)
    scales = (1,0.7,0.3,0.15)
    sizes = [ (size0[0] * sc, size0[1]*sc) for sc in scales]

    count = 0
    for sz in sizes:
        ten_s = scales[count] * 10
        start = time.process_time()
        if count == 3:
            param = { 'volume': False,'ylabel':"", 'ylabel_lower':"",'axisoff':True,
                      'update_width_config':{'line_width':0.4}}
            df = df.iloc[0:68]
            draw_candle_mpf(df, "", f'image/etf_{s}_{ten_s}.png', fsize=sz, other_param = param)
        else:
            draw_candle_mpf(df,f'ETF:{s}',f'image/etf_{s}_{ten_s}.png',fsize = sz)
        print(time.process_time() - start)
        count += 1

# def test_db_op():
#
#     conn = sqlite3.connect('etf.db')
#
#
#     #Create table #,index_code,index_name,date,open,high,low,close,vol,amount,change_pct
#     # c.execute('''CREATE TABLE daily_tick
#     #             (date text, open real,high real,low real,close real,volume real, adjLow real,adjClose real,
#     #             adjHigh real, adjOpen real, adjVolume, divCash, splitFactor, Symbol)''')
#     # #
#     for s in sector_etfs:
#         fn = f"data/{s}_2020-08-18.csv"
#         df = pd.read_csv(fn, parse_dates=True)
#         print("#")
#         df_to_db(conn, df)
#
#
#     conn.commit()
#     conn.close()





def test_draw_by_db():

    conn = sqlite3.connect('etf.db')
    #days: Set[int] = {89,111,123,134,145,156}
    days: Set[int] = { 111, 156}

    lls = [sector_etfs,industry_etfs,smartbeta_etfs, twenty1_century_etfs]
    #lls = [ishare_sector1_etf, ishare_sector2_etf]
    count = 0
    for ls in lls:
    #ls = smartbeta_etfs
        print("##Drawing batch %d"%count)
        for s in ls:
            for d in days:
                fn = f"image/sectors/etf_{s}_{d}.png"
                draw_chart_by_db(s,s,file=fn,connection=conn, days=d)
        count += 1


def test_harvest_missing():
    conn = sqlite3.connect('etf.db')
    lls = [ sector_etfs,industry_etfs,smartbeta_etfs,twenty1_century_etfs,ishare_sector1_etf,ishare_sector2_etf]
    count = 0
    for ls in lls:
        print("## start batch %d"%count)
        harvest_missing( ls ,conn)
        count += 1

    conn.commit()
    conn.close()

def test_init_harvest():
    delta = 225
    today = datetime.datetime.today()
    start = today - datetime.timedelta(days=delta)

    conn = sqlite3.connect('etf.db')


    #lls = [industry_etfs,smartbeta_etfs,twenty1_century_etfs ]
    lls = [ishare_sector1_etf,ishare_sector2_etf]
    for ls in lls:
        print("##" + str(ls))
        harvest(ls, conn, str(start))

    conn.commit()
    conn.close()



def main():
    #test_get_sectors()
    #test_draw_charts()
    #test_db_op()
    test_harvest_missing()
    test_draw_by_db()
    #test_init_harvest()

if __name__ == "__main__":
    main()