import tushare as ts
import pandas as pd
import sqlite3
import datetime
import time


fadd_postfix = lambda x: f'{x}.SH' if int(x) >= 600000 else f'{x}.SZ'

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

def get_a_stock_info(stock,start, end ,ts, connection=None , intodb=True):
    '''

    :param stock:
    :param start: start date , as format of 'yyyymmdd'
    :param end: end date , as format of 'yyyymmdd'
    :param connection:
    :return:
    '''
    #df = pro.index_daily(ts_code='600506.SI', start_date='20200101')
    #ts.set_token(token)
    #df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20200601', end_date='20201205')
    #today = datetime.datetime.today()
    if end == None:
        end = str(datetime.date.today())
    df = ts.pro_bar(ts_code=stock, adj='qfq', start_date=start, end_date=end)
    # round up very long value
    df['change'] = df['change'].apply(lambda x: round(x, 2))
    # change yyyymmdd to yyyy-mm-dd
    df['trade_date'] = df['trade_date'].apply(lambda x: f'{x[:4]}-{x[4:6]}-{x[6:]}')
    df = df.iloc[::-1] #reverse the order
    print(len(df.trade_date))
    df.to_csv(f'data/temp/{stock}.csv')


    if connection is None:
        conn = sqlite3.connect('sw_index.db')
    else:
        conn = connection

    if intodb:
        df.to_sql(name='stocks2', con=conn, index=False, if_exists='append')
    print("done get a stock info")


def get_list_of_stock_info(list, start, end,ts, conn = None):
    '''

    :param list:
    :param start:
    :param end:
    :param ts:
    :param conn:
    :return:
    '''
    for stk in list:
        time.sleep(1)
        stkp = fadd_postfix(stk)
        print(f"retriving {stk} as {stkp}")
        get_a_stock_info(stkp, start,end, ts,conn)