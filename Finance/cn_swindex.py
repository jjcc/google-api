# -*- coding: utf-8 -*-
from opendatatools import swindex
import pandas as pd
import plotly.graph_objects as go
import mplfinance as mpf
import matplotlib
import datetime
from time import sleep

list_file = "data/sw_index_class1"


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


#dump_sw_class1_list(list_file)


def get_class1_info(file):
    '''
    get list of SW class1 info
    :param file: The csv file containing SW class1 index dumped from other functions
    :return: list of class1 index data in form of (index, code, name)
    '''
    df_class_one = pd.read_csv(file)
    df_rec = df_class_one[['index_code','index_name']].to_records()
    tuple_list = [ x for x in df_rec]
    return tuple_list

def retrive_daily( info_tuple, start, end = None):
    '''
    retrieve data of an index.
    :param info_tuple:  The tuple about the index with the format of (index, code, name)
    :param start: start date string in format of 'yyyy-mm-dd'
    :param end:   end date string in format of 'yyyy-mm-dd'
    :return: data frame of the daily history
    '''
    if start == None:
        start = '2020-01-01'
    if end == None:
        end = str(datetime.date.today())
    df_daily,msg = swindex.get_index_daily(info_tuple[1],start,end)
    print(f'returned message: {msg}')
    return df_daily


# class1_list = get_class1_info(list_file)
# a_item = class1_list[1]
# a_daily = retrive_daily(a_item)
#
# fn = a_item[2]+ "_daily.csv"
#
# a_daily.to_csv("data/" + fn)

def harvest_daily_info(index_file, start_data, end_date = None, sleeptime = 0.0, stop=100 ):
    class1_list = get_class1_info(index_file)
    if end_date == None:
        end_date = str(datetime.date.today())
    count = 0
    for class1 in class1_list:
        a_item = class1
        fn = str(a_item[1])+ f'_till_{end_date}_daily.csv'
        a_daily = retrive_daily(a_item, start_data,end_date)
        a_daily.to_csv("data/" + fn)
        count += 1
        if count > stop:
            break
        if sleeptime > 0.0:
            sleep(sleeptime)







def draw_candle_plotly( df, image_file_name ):
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
    fig.write_image(image_file_name )




#draw_candle_plotly(df, img_file)

def draw_candle_mpf(df1, title = u"标题"):
    '''
    use mplfiance to draw chart
    :param df1:
    :return:
    '''
    cols = list(df1)
    cols.insert(0, cols.pop(cols.index('date')))
    df2 = df1.loc[:, cols]
    df2['date'] = pd.to_datetime(df2['date'])
    df3 = df2.set_index('date')

    mc = mpf.make_marketcolors(up='r', down='g')
    s = mpf.make_mpf_style(marketcolors=mc,rc={'font.family': 'SimHei'})#,'figure.facecolor':'lightgray'})

    mpf.plot(df3, type='candle', mav=(6, 12, 26),datetime_format='%Y-%m-%d',
             volume=True,
             title=title,style=s,
             tight_layout=True,
             ylabel=u'指数值',
             scale_padding={'bottom': 1.1,'left':0.8},
             #savefig='data/testsave_t.png')
             )

    #fig.savefig("pgf-mwe.png")




def draw_a_candle_image(row, today, data_file):
    code = row.name # it's 801030
    name = row.index_name
    title = f'{name}:{today}'
    df0 = pd.read_csv(data_file, parse_dates=True)
    df = df0.iloc[::-1, :]  # reverse the sequence
    old_cols = df.columns
    new_cols = [c if c != "vol" else "volume" for c in old_cols ]
    df.columns = new_cols
    dfsub = df #df.iloc[50:, :]
    draw_candle_mpf(dfsub, title)

def test_draw_candle():
    today = str(datetime.date.today())
    df_indexlist = pd.read_csv(list_file)

    # for index, row in df_indexlist.iterrows():
    #     code = row.index_code
    #     name = row.index_name
    #     title = f'{name}:{today}'
    code = 801030
    df_indexlist = df_indexlist.set_index('index_code')
    row = df_indexlist.loc[code,:]
    data_file = u'data/'+ f'{code}_till_{today}_daily.csv'
    print(data_file)

    draw_a_candle_image(row, today,data_file)

def main(arg):
    test_draw_candle()
#sample

#df_code = df_class_one['index_code']
#df_code_list = df_class_one['index_code'].to_list()
#df_cons, msg = swindex.get_index_cons('801040')
#df_daily, msg = swindex.get_index_daily('801040')

#pass
def test_harvest():
    today = datetime.datetime.today()
    start = today - datetime.timedelta(days=125) #shoudl do 135
    #print(str(start.date())) #output like '2020-03-04'
    harvest_daily_info(list_file,start_data=str(start.date()), sleeptime = 0.5, stop = 10)


if __name__ == "__main__":
    #arguments = parse_arguments()
    main(None)
    #test_harvest()
