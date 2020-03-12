import numpy as np
import pandas as pd
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import binance
import time
import datetime
from datetime import date
from binance.client import Client
import matplotlib.pyplot as plt
import csv
from talib import abstract
import talib


start = time.time()


#constant
today = date.today()
timestampStr = today.strftime("%d %b, %Y")
 #print(timestampStr)

api_key = 'hVvOTPoDT54u8CndCxam03axcJcaPZjWFAQv7wruzhK2PTeu80nt6mRkAeNkSAR9'
api_secret = 'E0PupiP3L94PxiWI0C6BUhzbLhLGwdHbroOUnB8lKyawmrEmWU5lasFndzHYSbCa'
client = Client(api_key, api_secret)
client = Client("api-key", "api-secret", {"verify": False, "timeout": 20})
date1 = '10 Dec, 2019'


klines_4hr = client.get_historical_klines('ETHUSDT', Client.KLINE_INTERVAL_4HOUR, '1 Feb, 2020')





#trade_price = client.get_recent_trades(symbol='ETHUSDT')[250]['price']
trade_time = client.get_recent_trades(symbol='ETHUSDT')[250]['time']
trades = client.get_recent_trades(symbol='ETHUSDT')

#get server time
Server_time = client.get_server_time()
#print(Server_time)



#print(Server_time)
#print(trade_price,trade_time)
#trades_df = pd.DataFrame(trades)
#trades_df.to_excel("trades_df.xlsx")
#trades_df.to_csv('trades_df.csv', encoding='utf-8')


# transform the data time
timeArray = time.localtime(int(trade_time)/1000)
trade_time_trans = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


# Create a Numpy array for trade price and trade time
#arr = np.array([trade_price,trade_time_trans])
#np.savetxt('trade_details.csv', [arr], delimiter=',', fmt='%s')


four_df = pd.DataFrame(klines_4hr)
four_df.columns = ['Open_time','open','high','low','close','volume','Close_time', 'Quote asset volume', 'number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
four_df = four_df.drop_duplicates(subset=['Open_time'], keep=False)
four_df = four_df.drop_duplicates(subset=['Close_time'], keep=False)

def transform_time(df):
    return df.apply(lambda d: datetime.datetime.fromtimestamp(int(d)/1000).strftime('%Y-%m-%d %H:%M:%S'))

# use lambda to  transfor the timestamp to local time 
four_df['Open_time_GST']=transform_time(four_df['Open_time'])
four_df['Close_time_GST'] = transform_time(four_df['Close_time'])


close = [float(x) for x in four_df['close']]

four_df['MACD'],four_df['MACDsignal'],four_df['MACDhist'] = talib.MACD(np.array(close),
                            fastperiod=12, slowperiod=26, signalperiod=9) 

four_df.sort_values(by=['Open_time'], inplace=True, ascending=False)
four_df.to_excel("binance_ETHUSDT_MACD.xlsx")

print(float(four_df['MACDhist'].iloc[0]))
if (float(four_df['MACDhist'].iloc[1]) < 0 and float(four_df['MACDhist'].iloc[0]) > 0 ):
    data = open('MACD_Signal.txt', 'w')
    data.write('1')
elif (float(four_df['MACDhist'].iloc[1]) > 0 and float(four_df['MACDhist'].iloc[0]) < 0 ):
    data = open('MACD_Signal.txt', 'w')
    data.write('2')
elif (float(four_df['MACDhist'].iloc[0]) > -0.5 or float(four_df['MACDhist'].iloc[0]) < 0.5 ):
    data = open('MACD_Signal.txt', 'w')
    data.write('3')

else:
    data = open('MACD_Signal.txt', 'w')
    data.write('0')
    
MyList = str(four_df['MACDhist'].iloc[0])
Price_now = str(four_df['close'].iloc[0])
MyFile=open('MACD.txt','w')
Price=open('Price.txt','w')
MyFile.writelines(MyList)
Price.writelines(Price_now)
MyFile.close()
Price.close()
end = time.time()

print('Execute-Time:',end-start)