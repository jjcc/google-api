import requests
import pandas as pd
import datetime
from datetime import datetime,timedelta
token1=""
with open("tiingo.token") as f:
    token1 = f.readline()

SP=pd.read_csv(r"data/SP500stocks.csv")


ticker_symbols=list(SP["Symbol"])


ticker_symbols.append("MSFT")
#start_date = datetime.now().date()-timedelta(days=2*365)
start_date = '2019-06-03'
end_date=str(datetime.now().date()-timedelta(days=1))
data1=[]

for symbol in ticker_symbols:
    #print (symbol)
    pass

   # #with rate_limiter:
   # try:
   #     url="https://api.tiingo.com/tiingo/daily/{}/prices?startDate=2000-01-03&endDate={}&format=csv&token={}".format(symbol,end_date,token1)
   #     r = requests.get(url,timeout=10)
   #     rows=r.text.split("\n")[1:-1]
   #     df=pd.DataFrame(rows)
   #     df=df.iloc[:,0].str.split(",",13,expand=True)
   #     df["Symbol"]=symbol
   #     data1.append(df)
   # except :
   #     pass

symbol = "MSFT"
url="https://api.tiingo.com/tiingo/daily/{}/prices?startDate={}&endDate={}&format=csv&token={}".format(symbol,start_date,end_date,token1)
print(url)
r = requests.get(url,timeout=10)
rows=r.text.split("\n")[1:-1]
df=pd.DataFrame(rows)
df=df.iloc[:,0].str.split(",",13,expand=True)
df["Symbol"]=symbol
data1.append(df)


print(len(ticker_symbols))
#
df_final=pd.concat(data1)
df_final.drop(df_final.iloc[:,6:13],axis=1,inplace=True)
df_final.to_csv(r"data/historicalMSFT_quotes2.csv",index=False)