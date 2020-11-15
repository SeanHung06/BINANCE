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
from position import retreive_Position
from position import Update_Position
from transform_time import transform_time

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


klines_4hr = client.get_historical_klines('ETHUSDT', Client.KLINE_INTERVAL_4HOUR, '25 Sep, 2020')

             
trade_price = client.get_recent_trades(symbol='ETHUSDT')[250]['price']
trade_time = client.get_recent_trades(symbol='ETHUSDT')[250]['time']
trades = client.get_recent_trades(symbol='ETHUSDT')

#get server time
Server_time = client.get_server_time()
#print(Server_time)



#print(Server_time)
#print(trade_price,trade_time)
trades_df = pd.DataFrame(trades)
trades_df.to_excel("./Data/trades_df.xlsx")
trades_df.to_csv('./Data/trades_df.csv', encoding='utf-8')


# transform the data time
timeArray = time.localtime(int(trade_time)/1000)
trade_time_trans = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


# Create a Numpy array for trade price and trade time
arr = np.array([trade_price,trade_time_trans])
np.savetxt('./Data/trade_details.csv', [arr], delimiter=',', fmt='%s')


four_df = pd.DataFrame(klines_4hr)
four_df.columns = ['Open_time','open','high','low','close','volume','Close_time', 'Quote asset volume', 'number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
four_df = four_df.drop_duplicates(subset=['Open_time'], keep=False)
four_df = four_df.drop_duplicates(subset=['Close_time'], keep=False)



# use lambda to  transfor the timestamp to local time 
four_df['Open_time_GST']=transform_time(four_df['Open_time'])
four_df['Close_time_GST'] = transform_time(four_df['Close_time'])


close = [float(x) for x in four_df['close']]

four_df['MACD'],four_df['MACDsignal'],four_df['MACDhist'] = talib.MACD(np.array(close),
                            fastperiod=12, slowperiod=26, signalperiod=9) 


    

Current_Pos = retreive_Position()
# Trying to predict the next Price to Corss MACD hist
for pa in range(int(float(trade_price)-50),int(float(trade_price)+50)):
    A = [float(x) for x in four_df['close']]
    predict = A[:-1]
    predict.append(pa)
    four_df['MACDpre'],four_df['MACDpresignal'],four_df['MACDprehis'] = talib.MACD(np.array(predict),
                            fastperiod=12, slowperiod=26, signalperiod=9) 
    if(four_df['MACDprehis'].iloc[-1]>1):
        print('Predict_price:',four_df['MACDprehis'].iloc[-1],pa)
        
        break
Predict_price = open('./Signal/Predict_price.txt', 'w')   
Predict_price.write(str(pa))

for ps in reversed(range(int(float(trade_price)-50),int(float(trade_price)+50))):
    S = [float(x) for x in four_df['close']]
    predict_sell = S[:-1]
    predict_sell.append(ps)
    four_df['MACD_sell'],four_df['MACD_sell_signal'],four_df['MACD_sell_his'] = talib.MACD(np.array(predict_sell),
                            fastperiod=12, slowperiod=26, signalperiod=9) 
    if(four_df['MACD_sell_his'].iloc[-1]<-1):
        print('Predict_Sell_price',four_df['MACD_sell_his'].iloc[-1],ps)
        break

Predict_sell_price = open('./Signal/Predict_sell_price.txt', 'w')   
Predict_sell_price.write(str(ps))




four_df.sort_values(by=['Open_time'], inplace=True, ascending=False)
four_df.to_excel("./Data/binance_ETHUSDT_MACD.xlsx")

print(float(four_df['MACDhist'].iloc[0]))

##Ready to Buy
if (float(four_df['MACDhist'].iloc[1]) < 1 and float(four_df['MACDhist'].iloc[0]) > 1 ):
    Ready_buy_time = time.time()
    Ready_buy_time_pre_data = open('./Signal/Ready_buy_time.txt', 'r')
    Ready_buy_time_pre = Ready_buy_time_pre_data.read()
    print("Ready_toBuy:",Ready_buy_time-float(Ready_buy_time_pre))
    if(Ready_buy_time-float(Ready_buy_time_pre)>1800) and  Current_Pos == '0':
        data_time = open('./Signal/Ready_buy_time.txt', 'w')
        data_time.write(str(Ready_buy_time))
        data = open('./Signal/MACD_Signal.txt', 'w')
        data.write('1')
    else:
        data = open('./Signal/MACD_Signal.txt', 'w')
        data.write('0')
##Ready to Sell
elif (float(four_df['MACDhist'].iloc[1]) > -1 and float(four_df['MACDhist'].iloc[0]) < -1 ):

    Ready_Sell_time = time.time()
    Ready_Sell_time_pre_data = open('./Signal/Ready_Sell_time.txt', 'r')
    Ready_Sell_time_data_pre = Ready_Sell_time_pre_data.read()
    print("Ready_Sell:",Ready_Sell_time-float(Ready_Sell_time_data_pre))
    if(Ready_Sell_time-float(Ready_Sell_time_data_pre)>1800) and  Current_Pos == '1':
        data_time = open('./Signal/Ready_Sell_time.txt', 'w')
        data_time.write(str(Ready_Sell_time))
        data = open('./Signal/MACD_Signal.txt', 'w')
        data.write('2')
    else:
        data = open('./Signal/MACD_Signal.txt', 'w')
        data.write('0')
        
## Sell        
elif (float(four_df['MACDhist'].iloc[2]) > -1 and float(four_df['MACDhist'].iloc[1]) < -1 and float(four_df['MACDhist'].iloc[0]) < -1 ):

    Sell_time = time.time()
    
    Sell_time_pre_data = open('./Signal/Sell_time.txt', 'r')
    Sell_time_data_pre = Sell_time_pre_data.read()
    print("Sell:",Sell_time-float(Sell_time_data_pre))
    if(Sell_time-float(Sell_time_data_pre)>1800):
        if Current_Pos == '1':
            Update_Position('0')
            data_time = open('./Signal/Sell_time.txt', 'w')
            data_time.write(str(Sell_time))
            data = open('./Signal/MACD_Signal.txt', 'w')
            data.write('5')
    else:
        data = open('./Signal/MACD_Signal.txt', 'w')
        data.write('0')
      
    
## Warning   

# elif ((float(four_df['MACDhist'].iloc[0]) > 0.49 and float(four_df['MACDhist'].iloc[0]) < 1) or (float(four_df['MACDhist'].iloc[0]) < -0.5 and float(four_df['MACDhist'].iloc[0]) > -1)):
#     Alert_time = time.time()
    
#     Alert_time_pre_data = open('./Signal/Alert_time.txt', 'r')
#     Alert_time_data_pre = Alert_time_pre_data.read()
#     print("Alert:",Alert_time-float(Alert_time_data_pre))
#     if(Alert_time-float(Alert_time_data_pre)>1800):
#         data_time = open('./Signal/Alert_time.txt', 'w')
#         data_time.write(str(Alert_time))
#         data = open('./Signal/MACD_Signal.txt', 'w')
#         data.write('3')
#     else:
#         data = open('./Signal/MACD_Signal.txt', 'w')
#         data.write('0')
##Buy
elif (float(four_df['MACDhist'].iloc[1]) > 1 and float(four_df['MACDhist'].iloc[0]) > 1  and float(four_df['MACDhist'].iloc[2]) < 1): 
    Buy_time = time.time()
    
    Buy_time_pre_data = open('./Signal/Buy_time.txt', 'r')
    Buy_time_data_pre = Buy_time_pre_data.read()
    print("Buy:",Buy_time-float(Buy_time_data_pre))
    if(Buy_time-float(Buy_time_data_pre)>1800):
        if Current_Pos == '0':
            Update_Position('1')
            data_time = open('./Signal/Buy_time.txt', 'w')
            data_time.write(str(Buy_time))
            data = open('./Signal/MACD_Signal.txt', 'w')
            data.write('4')
    else:
        data = open('./Signal/MACD_Signal.txt', 'w')
        data.write('0')
    
    
else:
    data = open('./Signal/MACD_Signal.txt', 'w')
    data.write('0')
    
MyList = str(four_df['MACDhist'].iloc[0])
Price_now = str(four_df['close'].iloc[0])
MyFile=open('./Signal/MACD.txt','w')
Price=open('./Signal/Price.txt','w')
MyFile.writelines(MyList)
Price.writelines(Price_now)
MyFile.close()
Price.close()
end = time.time()

print('Execute-Time:',end-start)