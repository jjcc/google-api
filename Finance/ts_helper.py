import tushare as ts
import pandas as pd
import sqlite3
import datetime
import time



def get_indices(pro):
    '''

    :param pro: tushare pro
    :return:
    '''
    markets = ['MSCI', 'CSI', 'SSE', 'SZSE', 'CICC', 'SW', 'OTH']
    for m in markets:
        df = pro.index_basic(market=m)
        leng = len(df)
        print(f"====length of {m}:{leng}====")
        df.to_csv(f"data/indices/{m}_index.csv")

def get_stock_list(pro):
    #df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,market,exchange,list_status,list_date')
    df = pro.query('stock_basic',exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,market,exchange,list_date')
    #print(len(df.ts_code))
    df.to_csv("data/temp/stock_list.csv")

def get_latest():
    conn = sqlite3.connect('sw_index2.db')

    c = conn.cursor()
    # SELECT max(date(trade_date)) as latest FROM stocks2 WHERE ts_code = '000505.SZ'
    c.execute("SELECT max(date(trade_date)) as latest FROM stocks2")
    row = c.fetchone()
    latest_str = row[0]
    print(latest_str)
