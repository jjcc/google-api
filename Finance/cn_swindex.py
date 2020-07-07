from opendatatools import swindex
import pandas as pd
import plotly.graph_objects as go
import mplfinance as mpf

list_file = "data/sw_index_class1"


def dump_sw_class1_list(file):
    '''
    Get the list of SW class1 list and save to file
    :param file:
    :return:
    '''
    df, msg = swindex.get_index_list()
    print(msg)
    df_class_one = df[df['section_name'] == u'一级行业']
    df_class_one.to_csv(file)


#dump_sw_class1_list(list_file)


def get_class1_info(file):
    df_class_one = pd.read_csv(file)
    df_rec = df_class_one[['index_code','index_name']].to_records()
    tuple_list = [ x for x in df_rec]
    # list of (index, code, name)
    return tuple_list

def retrive_daily( info_tuple):
    df_daily,msg = swindex.get_index_daily(info_tuple[1],'2020-01-01','2020-07-06')
    print(f'returned message: {msg}')
    return df_daily


# class1_list = get_class1_info(list_file)
# a_item = class1_list[1]
# a_daily = retrive_daily(a_item)
#
# fn = a_item[2]+ "_daily.csv"
#
# a_daily.to_csv("data/" + fn)







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



df = pd.read_csv(u'data/采掘_daily.csv')
img_file = u'data/采掘_daily.csv'


#draw_candle_plotly(df, img_file)

def draw_candle_mpf(df1):
    cols = list(df1)
    cols.insert(0, cols.pop(cols.index('date')))
    df2 = df1.ix[:, cols]
    df2['date'] = pd.to_datetime(df2['date'])
    df3 = df2.set_index('date')
    mpf.plot(df3, type='candle', mav=(5, 12, 26),datetime_format='%d-%B-%Y')


draw_candle_mpf(df)

#sample

#df_code = df_class_one['index_code']
#df_code_list = df_class_one['index_code'].to_list()
#df_cons, msg = swindex.get_index_cons('801040')
#df_daily, msg = swindex.get_index_daily('801040')

#pass

