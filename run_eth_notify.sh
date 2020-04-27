# 記錄一下開始時間
echo `date` >> /c/Users/USER/Desktop/python/BINANCE/log_notify &&
# 進入helloworld.py程式所在目錄
cd /c/Users/USER/Desktop/python/BINANCE &&
# 執行python指令碼（注意前面要指定python執行環境/usr/bin/python，根據自己的情況改變）
binance1.py
./MACD/get_Binance.py
email_price_notify.py
# 執行完成