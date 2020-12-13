# -*- coding: utf-8 -*-
from opendatatools import swindex
import pandas as pd
import plotly.graph_objects as go
import mplfinance as mpf
import matplotlib
import datetime
from time import sleep
import os
import sys, getopt
import sqlite3
import logging
import tushare as ts

logging.basicConfig(filename='swindex_app.log', filemode='a', level='INFO',
                    format='%(asctime)s  - %(levelname)s - %(message)s')
list_file = "data/sw_index_class1"

token = ""
#with open("tushare.token") as f:
#    token = f.readline()
#pro = ts.pro_api(token)

def dump_sw_class1_list(file):
    '''
    Get the list of SW class1 list and save to file
    :param file: the file containing indices that will be saved
    :return:
    '''
    df, msg = swindex.get_index_list()
    print(msg)
    df_class_one = df[df['section_name'] == u'一级行业']
    df_class_one.to_csv(file)


# dump_sw_class1_list(list_file)


def get_class1_info(file):
    '''
    get list of SW class1 info
    :param file: The csv file containing SW class1 index dumped from other functions
    :return: list of class1 index data in form of (index, code, name)
    '''
    df_class_one = pd.read_csv(file)
    df_rec = df_class_one[['index_code', 'index_name']].to_records()
    tuple_list = [x for x in df_rec]
    return tuple_list


def dump_components(index_file, sleeptime=0.0, stop=100):
    '''
    dump all components of indices
    :param index_file:
    :param sleeptime:
    :param stop:
    :return:
    '''
    class1_list = get_class1_info(index_file)
    count = 0
    cnt_comp = 0
    for class1 in class1_list:
        a_item = class1

        code = a_item[1]
        df_comp, msg = swindex.get_index_cons(str(code))
        leng_df = len(df_comp.index)
        cnt_comp += leng_df
        print(f'current{code} has components of {leng_df}/{cnt_comp}(in total)')
        fn = str(a_item[1]) + f'_components.csv'
        df_comp.to_csv("data/comp/" + fn)
        count += 1
        if count > stop:
            break
        if sleeptime > 0.0:
            sleep(sleeptime)


def retrive_a_daily(code_info, start, end=None):
    '''
    retrieve data of an index.
    :param code_info:  The tuple about the index with the format of (index, code, name)
    :param start: start date string in format of 'yyyy-mm-dd'
    :param end:   end date string in format of 'yyyy-mm-dd'
    :return: data frame of the daily history
    '''
    if start == None:
        start = '2020-01-01'
    if end == None:
        end = str(datetime.date.today())
    if isinstance(code_info, tuple):
        df_daily, msg = swindex.get_index_daily(code_info[1], start, end)
    else:
        code_list = [ str(code[1]) for code in code_info]
        df_daily, msg = swindex.get_index_daily(code_list, start, end)

    print(f'returned message: {msg}')
    return df_daily


def harvest_daily_info(index_file, start_data, end_date=None, sleeptime=0.0, stop=100):
    '''
    Harvest daily info and save into csv files
    call: get_class1_info(), retrive_a_daily()

    :param index_file: the file contains the indices
    :param start_data: start date of indices data
    :param end_date: end date of indices data
    :param sleeptime: sleep between 2 scraping. unit in seconds
    :param stop: For test only, the number for stop
    :return:
    '''
    class1_list = get_class1_info(index_file)
    if end_date == None:
        end_date = str(datetime.date.today())
    # count = 0
    # all_daily = None
    # test = True
    # if test:

    ###!!!With modification of swindex in opendatatools
    all_daily = retrive_a_daily(class1_list, start_data, end_date)
    return all_daily

    # for class1 in class1_list:
    #     a_item = class1
    #     fn = str(a_item[1]) + f'_till_{end_date}_daily.csv'
    #     a_daily = retrive_a_daily(a_item, start_data, end_date)
    #     if all_daily is None:
    #         all_daily = a_daily
    #     else:
    #         all_daily = all_daily.append(a_daily)
    #
    #     # a_daily.to_csv(f"data/{end_date}/" + fn)
    #     count += 1
    #     if count > stop:
    #         break
    #     if sleeptime > 0.0:
    #         sleep(sleeptime)
    # return all_daily


def draw_candle_plotly(df, image_file_name):
    trace1 = {
        'x': df.index,
        'open': df.open,
        'close': df.close,
        'high': df.high,
        'low': df.low,
        'type': 'candlestick',
        'name': '采掘',
        'showlegend': False
    }
    # Calculate and define moving average of 30 periods
    avg_30 = df.close.ewm(span=30, min_periods=1).mean()
    # Calculate and define moving average of 50 periods
    avg_50 = df.close.ewm(span=50, min_periods=1).mean()
    avg_12 = df.close.ewm(span=12, min_periods=1).mean()
    trace2 = {
        'x': df.index,
        'y': avg_30,
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'blue'
        },
        'name': 'Moving Average of 30 periods'
    }
    trace3 = {
        'x': df.index,
        'y': avg_50,
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'red'
        },
        'name': 'Moving Average of 50 periods'
    }
    trace4 = {
        'x': df.index,
        'y': avg_12,
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'cyan'
        },
        'name': 'Moving Average of 12 periods'
    }
    data = [trace1, trace2, trace3, trace4]
    # Config graph layout
    layout = go.Layout({
        'title': {
            'text': 'Microsoft(MSFT) Moving Averages',
            'font': {
                'size': 15
            }
        }
    })
    fig = go.Figure(data=data, layout=layout)
    fig.write_image(image_file_name)


# draw_candle_plotly(df, img_file)

def draw_candle_mpf(a_index_df, title="", image_file="test.png", fsize = None,other_param=None):
    '''
    use mplfiance to draw chart
    :param a_index_df: the dataframe of a index
    :param title: title of the image
    :param image_file: the output image file
    :return:
    '''
    cols = list(a_index_df)
    cols.insert(0, cols.pop(cols.index('date')))
    df2 = a_index_df.loc[:, cols]
    df2['date'] = pd.to_datetime(df2['date'])
    df3 = df2.set_index('date')

    mc = mpf.make_marketcolors(up='r', down='g')
    s = mpf.make_mpf_style(marketcolors=mc, rc={'font.family': 'SimHei'})  # ,'figure.facecolor':'lightgray'})

    if os.path.isfile(image_file):
        os.remove(image_file)

    yl = u'值'
    yll = u'成交量'
    v = True
    xoff = False
    uwc = None #{"dummy":0}
    if fsize == None:
        fsize = (8.0, 5.75)
    if other_param != None:
        yl = other_param.get('ylabel')
        yll = other_param.get('ylabel_lower')
        v = other_param.get('volume')
        xoff = other_param.get('axisoff')
        uwc = other_param.get('update_width_config')
        mpf.plot(df3, type='candle', mav=(6, 12, 26), datetime_format='%Y-%m-%d',
             volume=v,
             title=title, style=s,
             tight_layout=True,
             ylabel= yl,
             ylabel_lower= yll,
             scale_padding={'bottom': 1.1, 'left': 0.8},
             savefig=image_file,
             figsize=fsize,
             axisoff=xoff,
             update_width_config = uwc)
    else:
        mpf.plot(df3, type='candle', mav=(6, 12, 26), datetime_format='%Y-%m-%d',
             volume=v,
             title=title, style=s,
             tight_layout=True,
             ylabel= yl,
             ylabel_lower= yll,
             scale_padding={'bottom': 1.1, 'left': 0.8},
             savefig=image_file,
             figsize=fsize,
             axisoff=xoff)

    # fig.savefig("pgf-mwe.png")


def draw_a_candle_image(row, today, data_file, image_file="test.png"):
    """
    Draw one candle image
    :param row:
    :param today:
    :param data_file:
    :param image_file:
    :return:
    """
    code = row.name  # it's like 801030
    name = row.index_name
    title = f'{name}:{today}'
    df0 = pd.read_csv(data_file, parse_dates=True)
    df = df0.iloc[::-1, :]  # reverse the sequence
    old_cols = df.columns
    new_cols = [c if c != "vol" else "volume" for c in old_cols]
    df.columns = new_cols
    dfsub = df  # df.iloc[50:, :]
    draw_candle_mpf(dfsub, title, image_file)


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
        f'select *  from class1_index where index_code = \'{code}\'   ORDER BY date(date) DESC limit 89', conn)
    df0 = pd.DataFrame(SQL_Query)
    df = df0.iloc[::-1, :]  # reverse the sequence

    today = str(datetime.date.today())

    title = f'{name}:{today}'
    old_cols = df.columns
    new_cols = [c if c != "vol" else "volume" for c in old_cols]
    df.columns = new_cols
    dfsub = df  # df.iloc[50:, :]
    draw_candle_mpf(dfsub, title, file)


# def test_retreive_a_daily():
#     class1_list = get_class1_info(list_file)
#     a_item = class1_list[1]
#     a_daily = retrive_a_daily(a_item)
#     fn = a_item[2] + "_daily.csv"
#     a_daily.to_csv("data/" + fn)


def harvest_missing(connection=None, test = False):
    """
    filling the missing data into db
    :return: dataframe of missing data in db
    """
    today = datetime.datetime.today()
    if connection is None:
        conn = sqlite3.connect('sw_index.db')
    else:
        conn = connection

    c = conn.cursor()
    c.execute("SELECT max(date(date)) as latest FROM class1_index;")
    latest_str = c.fetchone()[0]

    # if test:
    #     latest_str = '2020-08-24'

    # print(latest_str)
    latest_date = datetime.datetime.strptime(latest_str, "%Y-%m-%d")
    latest_date_next = latest_date + datetime.timedelta(days=1)
    leatest_str_next = datetime.datetime.strftime(latest_date_next, "%Y-%m-%d")
    # print(leatest_str_next)

    today = datetime.datetime.today()
    end = today + datetime.timedelta(days=1)

    if leatest_str_next == str(end.date()):
        return None
    # start = latest
    df = harvest_daily_info(list_file,
                            start_data=leatest_str_next,
                            end_date=str(end.date()),
                            sleeptime=0.5) #,
                            #stop = 3)
    if len(df)  == 0:
        if connection is None:  # This means conn was initialized inside this function
            conn.close()
        return df
    df['date'].apply(str)
    for index, row in df.iterrows():
        row['date'] = datetime.datetime.strftime(row['date'], "%Y-%m-%d")
        c.execute(
            "INSERT INTO class1_index([index_code],[date], [open],[high],[low],[close],[vol],[amount],[change_pct]) values(?,?,?,?,?,?,?,?,?)",
            (row['index_code'], row['date'],
             row['open'], row['high'], row['low'], row['close'],
             row['vol'], row['amount'], row['change_pct']))

    conn.commit()
    c.close()
    if connection is None:  # This means conn was initialized inside this function
        conn.close()

    return df


def dbdraw(connection=None):
    '''
    Draw candle images from DB data
    :param connection:
    :return:
    '''
    today = str(datetime.date.today())
    logging.info(f'{today} draw images')

    df_indexlist = pd.read_csv(list_file)

    # for index, row in df_indexlist.iterrows():
    #     code = row.index_code
    #     name = row.index_name
    #     title = f'{name}:{today}'
    df_indexlist = df_indexlist.set_index('index_code')
    code_list = df_indexlist.index.tolist()

    for code, row in df_indexlist.iterrows():
        name = row["index_name"]
        print(u"code:%d, name:%s" % (code, name))
        image_file = f'image/cw_index/{code}_current.png'
        draw_chart_by_db(code, name, image_file, connection)

def get_all_stock_info(file=None):
    df_close = ts.get_today_all()
    if file == None:
        file = u"data/meta/all_stocks_close.csv"
    df_close.to_csv(file)

def test_draw_candle():
    today = str(datetime.date.today())
    df_indexlist = pd.read_csv(list_file)

    # for index, row in df_indexlist.iterrows():
    #     code = row.index_code
    #     name = row.index_name
    #     title = f'{name}:{today}'
    df_indexlist = df_indexlist.set_index('index_code')

    today = str(datetime.date.today())
    data_dir = f'data/{today}/'
    files_under_data = os.listdir(data_dir)
    for f in files_under_data:
        if f.endswith(".csv") and "daily" in f:
            seg = f.split("_")
            code = seg[0]
            code_num = int(code)
            row = df_indexlist.loc[code_num, :]
            print(f'{f},{code_num}')
            data_file = data_dir + f
            image_file = f'image/{today}/{code_num}_current.png'
            draw_a_candle_image(row, today, data_file, image_file)

    draw_a_candle_image(row, today, data_file)


def test_get_components():
    dump_components(list_file, sleeptime=0.8)


# sample

# df_code = df_class_one['index_code']
# df_code_list = df_class_one['index_code'].to_list()
# df_cons, msg = swindex.get_index_cons('801040')
# df_daily, msg = swindex.get_index_daily('801040')

# pass
def test_harvest():
    today = datetime.datetime.today()
    start = today - datetime.timedelta(days=125)  # shoudl do 135
    # print(str(start.date())) #output like '2020-03-04'
    harvest_daily_info(list_file, start_data=str(start.date()), sleeptime=0.5, stop=10)


def test_harvest_missing():
    df = harvest_missing()


def test_cvs2db():
    conn = sqlite3.connect('sw_index.db')
    c = conn.cursor()

    # Create table #,index_code,index_name,date,open,high,low,close,vol,amount,change_pct
    # c.execute('''CREATE TABLE class1_index
    #             ( index_code text,date text, open real,high real,low real,close real,vol real, amount real,change_pct real)''')
    # data_file = "data/2020-08-10/801010_till_2020-08-11_daily.csv"
    today = str(datetime.date.today())
    data_dir = f'data/{today}/'
    files_under_data = os.listdir(data_dir)
    for f in files_under_data:
        if f.endswith(".csv") and "daily" in f:
            data_file = data_dir + f
            df = pd.read_csv(data_file, parse_dates=True)
            for index, row in df.iterrows():
                c.execute(
                    "INSERT INTO class1_index([index_code],[date], [open],[high],[low],[close],[vol],[amount],[change_pct]) values(?,?,?,?,?,?,?,?,?)",
                    (row['index_code'], row['date'],
                     row['open'], row['high'], row['low'], row['close'],
                     row['vol'], row['amount'], row['change_pct']))

    conn.commit()
    c.close()
    conn.close()


def test_dbdraw():
    dbdraw()

def process_comp():
    logging.info("processing components")
    df_close = pd.read_csv(u"data/meta/all_stocks_close.csv",dtype = {"code" : "str"})
    #df_close = df_close.set_index('code')
    df_change = df_close[['code', 'changepercent']]
    df_indexlist = pd.read_csv(list_file)
    df_indexlist = df_indexlist.set_index('index_code')
    for code, row in df_indexlist.iterrows():
        name = row["index_name"]
        print(u"code:%d, name:%s" % (code, name))
        cvs_file = f'data/comp/{code}_components.csv'
        json_file = f'data/compj/{code}_componentsx.json'


        #file = 'data/comp/801010_components.csv'
        df_comp_one = pd.read_csv(cvs_file,dtype = {"stock_code" : "str"},index_col= 0)
        df_selected = df_comp_one[['stock_code', 'stock_name', 'weight']]
        if True:

            df_all = pd.merge(left=df_selected, right=df_change, left_on='stock_code',right_on='code', how='left')
            df_all.sort_values("changepercent", ascending=False, inplace=True)
            df_all.reset_index(drop=True,inplace=True)
            df_all.to_json(json_file)

        #df_selected.to_json(json_file)

    pass

def run_app():
    """
    Default routine run by main()
    :return:
    """
    try:
        conn = sqlite3.connect('sw_index.db')
    except Exception as e:
        logging.error("Exception occurred when open db", exc_info=True)
        return

    if harvest_missing(conn) is None:
        conn.close()
        return
    print("getting all stock info")
    get_all_stock_info()
    print("processing components")
    process_comp()

    dbdraw(conn)
    conn.close()


def main(argv):
    # parameter as : "-a h" or "-a d" for action harvest or draw
    opts, args = getopt.getopt(argv, "a:", ["action="])

    if (len(opts) == 0):
        run_app()
        return

    for opt, arg in opts:
        if opt == '-a':
            action = arg
    if action == 'h':  # harvest
        today = datetime.datetime.today()
        end = today + datetime.timedelta(days=1)
        start = today - datetime.timedelta(days=135)
        # print(str(start.date())) #output like '2020-03-04'
        harvest_daily_info(list_file,
                           start_data=str(start.date()),
                           end_date=str(end.date()),
                           sleeptime=0.5
                           )
        return
    if action == 'd':
        test_draw_candle()
    if action == 'c':
        test_get_components()
    if action == "cls1":
        dump_sw_class1_list(list_file)
    if action == "db":
        test_cvs2db()
    if action == 'dd':
        test_dbdraw()
    if action == "hm":
        test_harvest_missing()
    if action == "cm":
        process_comp()

if __name__ == "__main__":
    # arguments = parse_arguments()
    logging.info("<<run cn_swindex start")
    main(sys.argv[1:])
    logging.info("<<run cn_swindex end")
    # test_harvest()
