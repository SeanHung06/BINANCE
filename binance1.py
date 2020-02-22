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

#constant
today = date.today()
timestampStr = today.strftime("%d %b, %Y")
#print(timestampStr)

api_key = 'hVvOTPoDT54u8CndCxam03axcJcaPZjWFAQv7wruzhK2PTeu80nt6mRkAeNkSAR9'
api_secret = 'E0PupiP3L94PxiWI0C6BUhzbLhLGwdHbroOUnB8lKyawmrEmWU5lasFndzHYSbCa'
client = Client(api_key, api_secret)
client = Client("api-key", "api-secret", {"verify": False, "timeout": 20})
date1 = '10 Dec, 2019'


klines = client.get_historical_klines('ETHUSDT', Client.KLINE_INTERVAL_1DAY, '10 Aug, 2016')
klines_4hr = client.get_historical_klines('ETHUSDT', Client.KLINE_INTERVAL_4HOUR, '10 Aug, 2016')

signal = 0 
#constant


trade_price = client.get_recent_trades(symbol='ETHUSDT')[250]['price']
trade_time = client.get_recent_trades(symbol='ETHUSDT')[250]['time']
trades = client.get_recent_trades(symbol='ETHUSDT')
#get server time
Server_time = client.get_server_time()
#print(Server_time)
lambda Server_time: datetime.datetime.fromtimestamp(int(Server_time)/1000).strftime('%Y-%m-%d %H:%M:%S')
#print(Server_time)
#print(trade_price,trade_time)
trades_df = pd.DataFrame(trades)
#trades_df.to_excel("trades_df.xlsx")
trades_df.to_csv('trades_df.csv', encoding='utf-8')


# transform the data time
timeArray = time.localtime(int(trade_time)/1000)
trade_time_trans = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


# Create a Numpy array for trade price and trade time
arr = np.array([trade_price,trade_time_trans])
np.savetxt('trade_details.csv', [arr], delimiter=',', fmt='%s')




# use panda data frame to process the Kline data 
whole_df = pd.DataFrame(klines)
four_df = pd.DataFrame(klines_4hr)

whole_df.columns = ['Open_time','open','high','low','close','volume','Close_time', 'Quote asset volume', 'number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
four_df.columns = ['Open_time','open','high','low','close','volume','Close_time', 'Quote asset volume', 'number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']



whole_df = whole_df.drop_duplicates(subset=['Open_time'], keep=False)
four_df = four_df.drop_duplicates(subset=['Open_time'], keep=False)
four_df = four_df.drop_duplicates(subset=['Close_time'], keep=False)


# use lambda to  transfor the timestamp to local time 
whole_df['Open_time_GST']=whole_df['Open_time'].apply(lambda d: datetime.datetime.fromtimestamp(int(d)/1000).strftime('%Y-%m-%d %H:%M:%S'))
four_df['Open_time_GST']=four_df['Open_time'].apply(lambda d: datetime.datetime.fromtimestamp(int(d)/1000).strftime('%Y-%m-%d %H:%M:%S'))
four_df['Close_time_GST']=four_df['Close_time'].apply(lambda d: datetime.datetime.fromtimestamp(int(d)/1000).strftime('%Y-%m-%d %H:%M:%S'))


#get the Moving average for 7 days 15 days 30 days
whole_df['MA_1'] = whole_df['close'].rolling(1).mean()
whole_df['MA_2'] = whole_df['close'].rolling(2).mean()
whole_df['MA_7'] = whole_df['close'].rolling(7).mean()
whole_df['MA_15'] = whole_df['close'].rolling(15).mean()
whole_df['MA_30'] = whole_df['close'].rolling(30).mean()


#get the Exponetial Moving average for 7 days 15 days 30 days

whole_df['EMA_1'] = whole_df['close'].ewm(span=1).mean()
whole_df['EMA_2'] = whole_df['close'].ewm(span=2).mean()
whole_df['EMA_12'] = whole_df['close'].ewm(span=12).mean()
whole_df['EMA_26'] = whole_df['close'].ewm(span=26).mean()


whole_df['DIF'] = whole_df['EMA_12'] - whole_df['EMA_26']
whole_df['DEM'] = whole_df['DIF'].ewm(span=9).mean()
whole_df['OSC'] = whole_df['DIF'] - whole_df['DEM']



# drawing the plots for the EMA
#fig,ax = plt.subplots(5,1,figsize=(10,10))
#plt.subplots_adjust(hspace=0.5)
#whole_df['EMA_1'].plot(ax=ax[0])
#whole_df['EMA_26'].plot(ax=ax[1])
#plt.plot(whole_df['Open_time_GST'],whole_df['EMA_1'])

#ax[0].legend()
#ax[1].legend()
#plt.show() 


EMA1 = whole_df['EMA_1'][whole_df['EMA_1'].size-1]
EMA2 = whole_df['EMA_2'][whole_df['EMA_2'].size-1]

data = open('data.txt', 'r')

# read and write the EMA file
MyList = [str(EMA1),'\n',str(EMA2)]

MyFile=open('EMA.txt','w')
MyFile.writelines(MyList)
MyFile.close()


print(EMA1,EMA2,whole_df['EMA_1'].size)
signal_temp = data.read()
if EMA1 > EMA2 :
    signal = 1
    data = open('data.txt', 'w')
    data2 = open('buy_sell.txt', 'w')
    data2.write('0')
    data.write(str(signal))
    data.close()
    data2.close()

if EMA1 < EMA2:
    signal = 2
    data1 = open('data.txt', 'w')
    data2 = open('buy_sell.txt', 'w')
    data1.write(str(signal))
    data2.write('1')
    data1.close()
    data2.close()

if(signal_temp != str(signal)):
    email_data = open('email_send_signal.txt', 'w')
    email_data.write(str(1))

    
#drop the rest columns
whole_df= whole_df.drop(columns=['Ignore', 'Open_time'])
# drop the rows in whole_df and keep the bottom 10 

#######STUCK###
#whole_df = whole_df.drop(whole_df.head())


whole_df.to_excel("binance_ETHUSDT_data.xlsx")
whole_df.to_csv('binance_ETHUSDT_data.csv', encoding='utf-8')




