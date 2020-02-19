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


abstract.SMA(whole_df,5)