import tushare as ts
import pandas as pd

# data = ts.get_hist_data('600848',start='2020-01-01')

token = ""
with open("tushare.token") as f:
    token = f.readline()
pro = ts.pro_api(token)


def get_indices():
    markets = ['MSCI', 'CSI', 'SSE', 'SZSE', 'CICC', 'SW', 'OTH']
    for m in markets:
        df = pro.index_basic(market=m)
        leng = len(df)
        print(f"====length of {m}:{leng}====")
        df.to_csv(f"data/indices/{m}_index.csv")



def get_all_stock_basics():
    df_basics = ts.get_stock_basics()
    df_basics.to_csv(u"data/meta/all_stocks_basics.csv")
    print("done with get all")

def get_all_stock_info():
    df_close = ts.get_today_all()
    #df_all = pd.merge(left=df_close, right=df_basics, on='name', how='outer')
    #df_all.to_csv(u"data/meta/all_stocks.csv")
    df_close.to_csv(u"data/meta/all_stocks_close.csv")



# df = pro.index_basic(market='SW')
# df = pro.index_daily(ts_code='801210.SI', start_date='20180101',end_date='20181001' )
# print(len(df.index))
# df.to_cvs("801193SI.csv")


def main():
    print(ts.__version__)
    #get_indices()
    get_all_stock_info()

if __name__ == "__main__":
    main()