#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from pandas_datareader import data as web
import plotly.graph_objects as go
'''
Generate a candle stick graphy
'''


stock = 'MSFT'
df = web.DataReader(stock, data_source='yahoo', start='06-01-2019')
df.to_csv('data/test.csv')

trace1 = {
    'x': df.index,
    'open': df.Open,
    'close': df.Close,
    'high': df.High,
    'low': df.Low,
    'type': 'candlestick',
    'name': 'MSFT',
    'showlegend': False
}
# Calculate and define moving average of 30 periods
avg_30 = df.Close.rolling(window=30, min_periods=1).mean()
# Calculate and define moving average of 50 periods
avg_50 = df.Close.rolling(window=50, min_periods=1).mean()

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

data = [trace1, trace2, trace3]
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
fig.write_html("Microsoft(MSFT) Moving Averages.html")
fig.show()


