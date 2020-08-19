# -*- coding: utf-8 -*-

from .cn_swindex import draw_chart_by_db
import requests
import pandas as pd
import datetime
from datetime import datetime,timedelta

token1=""
with open("tiingo.token") as f:
    token1 = f.readline()

sector_etfs = {"XLC","XLP","XLY","XLE","XLF","XLV","XLI","XLB","XLRE","XLK","XLU","XLSR"}
twenty1_century_etfs = {"KOMP","SIMS","HAIL","FITE","ROKT","CNRG"}
industry_etfs = {"KBE","KRE","KCE","KIE","XAR","XTN","XBI","XPH","XHE","XHS",
                 "XOP","XES","XME","XRT","XHB","XSD","XSW","XNTK","XITK","XTL","XWEB"}



data1=[]

symbol = "MSFT"




def get_quote_info(symbol, start_date, end_date, file_name ):

    url = "https://api.tiingo.com/tiingo/daily/{}/prices?startDate={}&endDate={}&format=csv&token={}".format(symbol,
                                                                                                             start_date,
                                                                                                             end_date,
                                                                                                             token1)
    print(url)
    r = requests.get(url, timeout=10)
    rows = r.text.split("\n")[1:-1]
    df = pd.DataFrame(rows)
    df = df.iloc[:, 0].str.split(",", 13, expand=True)
    df["Symbol"] = symbol
    data1.append(df)
    #
    df_final = pd.concat(data1)
    df_final.drop(df_final.iloc[:, 6:13], axis=1, inplace=True)
    df_final.to_csv(file_name, index=False)

    return df_final



def test_get_sectors():
    start_date = '2019-06-03'
    end_date = str(datetime.now().date() - timedelta(days=1))

    #fn = r"data/historicalMSFT_quotes2.csv"
    for s in sector_etfs:
        fn = f"data/{s}_{end_date}.csv"
        get_quote_info(s, start_date,end_date,fn)


if __name__ == "__main__":
    test_get_sectors()