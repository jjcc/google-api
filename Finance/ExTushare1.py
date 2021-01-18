import tushare as ts
import pandas as pd
import sqlite3
import datetime
import time

from ts_helper import *
from cn_swindex import draw_candle_mpf

# data = ts.get_hist_data('600848',start='2020-01-01')

token = ""
with open("tushare.token") as f:
    token = f.readline()
pro = ts.pro_api(token)


fadd_postfix = lambda x: f'{x}.SH' if int(x) >= 600000 else f'{x}.SZ'



def get_all_stock_basics():
    df_basics = ts.get_stock_basics()
    df_basics.to_csv(u"data/meta/all_stocks_basics.csv")
    print("done with get all")

def get_all_stock_info(file=None):
    ts.set_token(token)
    df_close = ts.get_today_all()
    #df_all = pd.merge(left=df_close, right=df_basics, on='name', how='outer')
    #df_all.to_csv(u"data/meta/all_stocks.csv")
    if file == None:
        file = u"data/meta/all_stocks_close.csv"
    df_close.to_csv(file)

SW_LIST = {}
def load_meta():
    list_file ='data/sw_index_class1'
    df_indexlist = pd.read_csv(list_file)
    df_indexlist = df_indexlist.set_index('index_code')
    for code, row in df_indexlist.iterrows():
        name = row["index_name"]
        print(u"code:%d, name:%s" % (code, name))
        cvs_file = f'data/comp/{code}_components.csv'
        #file = 'data/comp/801010_components.csv'
        df_comp_one = pd.read_csv(cvs_file,dtype = {"stock_code" : "str"},index_col= 0)
        df_selected = df_comp_one[['stock_code', 'stock_name', 'weight']]
        SW_LIST[code] = df_selected



def draw_chart_by_db(code, name, file, connection=None):
    """
    Draw a chart with data from DB
    Called by: dbdraw()
    Call: draw_candle_mpf()

    :param file:
    :param connection:
    :param code:
    :param name:
    :return:
    """
    if connection is None:
        conn = sqlite3.connect('sw_index.db')
    else:
        conn = connection
    c = conn.cursor()

    SQL_Query = pd.read_sql_query(
        f'select *  from stocks2 where ts_code = \'{code}\'   ORDER BY date(trade_date) DESC limit 89', conn)
    df0 = pd.DataFrame(SQL_Query)
    df = df0.iloc[::-1, :]  # reverse the sequence

    df = df.rename(columns={'trade_date': 'date'})
    today = str(datetime.date.today())

    title = f'{name}:{today}'
    old_cols = df.columns
    new_cols = [c if c != "vol" else "volume" for c in old_cols]
    df.columns = new_cols
    dfsub = df  # df.iloc[50:, :]
    draw_candle_mpf(dfsub, title, file)

# df = pro.index_basic(market='SW')
def test_getastock():
    conn = sqlite3.connect('sw_index2.db')
    get_a_stock_info('603566.SH','20201201',None,ts,conn, intodb=False)



def test_getlistofstocks():
    conn = sqlite3.connect('sw_index2.db')
    ts.set_token(token)
    load_meta()
    stock_list = SW_LIST[801010]['stock_code'].to_list()

    get_list_of_stock_info(stock_list,'20200401',None,ts,conn)


def do_drawlistofstocks():
    conn = sqlite3.connect('sw_index2.db')
    load_meta()
    df_sector = SW_LIST[801010]
    stock_list = df_sector['stock_code'].to_list()
    for stk in stock_list:
        stkp = fadd_postfix(stk)
        #name = 'aa' #df_sector['stock_code'][]
        name = df_sector['stock_name'][df_sector['stock_code'] == stk].to_list()[0]
        file = f'image/stocks/801010/{stk}.png'
        print(f"drawing {stk} as {stkp}")
        draw_chart_by_db(stkp,name,file,conn)


def test_get_all_stocks_lastday():
    get_all_stock_info(u'data/temp/all_stocks_lastday.cvs')



def test_load_lastday():
    load_meta()
    df_sector = SW_LIST[801010]
    stock_list = df_sector['stock_code'].to_list()
    today = datetime.date.today()
    #today = datetime.datetime.today()

    today_str = str(today)

    load_lastday_to_db(u'data/temp/all_stocks_lastday.cvs',stock_list,today_str)




def main():
    print(ts.__version__)
    #get_indices()
    #get_all_stock_info()
    #get_stock_list()
    #get_latest()
    #test_getastock()
    #test_getlistofstocks()
    ###############
    #test_get_all_stocks_lastday()
    file=u'data/temp/all_stocks_lastday.cvs'
    get_all_stock_info(file)
    print("##Step1:Got all stocks last day")
    #test_load_lastday()
    load_meta()
    df_sector = SW_LIST[801010]
    stock_list = df_sector['stock_code'].to_list()
    today_str = '2020-12-21'#str(datetime.date.today())
    load_lastday_to_db(file,stock_list,today_str)
    print("##Step2:all stocks last day loaded to DB")
    do_drawlistofstocks()
    print("##Step3:all stocks drawn")

if __name__ == "__main__":
    main()