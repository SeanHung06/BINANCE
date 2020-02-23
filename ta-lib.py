from talib import abstract
from binance1 import * 
import numpy as np
import pandas as pd
import talib

# 透過『get_functions』語法，查看 TA-Lib 提供的所有技術指標的代碼
all_ta_label = talib.get_functions()
# 看一下清單
#print(all_ta_label)
# 共有 158 個技術指標可以運算
len(all_ta_label)
a = talib.ADX(whole_df['high'],whole_df['low'],whole_df['close'],timeperiod = 14)


EMA = talib.EMA(whole_df['close'])
print(EMA)

EMA.to_excel("EMA.xlsx")
#MACD = talib.MACD(whole_df['close'],fastperiod=6, slowperiod=12, signalperiod=9)
#print(MACD)
#MACD.to_excel("MACD.xlsx")


close = [float(x) for x in four_df['close']]

four_df['MACD'],four_df['MACDsignal'],four_df['MACDhist'] = talib.MACD(np.array(close),
                            fastperiod=6, slowperiod=12, signalperiod=9) 

four_df.sort_values(by=['Open_time'], inplace=True, ascending=False)
four_df.to_excel("binance_ETHUSDT_MACD.xlsx")

ax = plt.gca()

four_df.plot(kind='line',y='MACD',ax=ax)
#four_df.plot(kind='line',y='close',ax=ax)

plt.show()