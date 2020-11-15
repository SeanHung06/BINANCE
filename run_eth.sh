# 記錄一下開始時間
echo `date` >> /Users/seanhung06/Binance/Logs/log &&
# 進入helloworld.py程式所在目錄
cd /Users/seanhung06/Binance &&
# 執行python指令碼（注意前面要指定python執行環境/usr/bin/python，根據自己的情況改變）
#/usr/local/bin/python3 binance1.py
/usr/local/bin/python3 ./MACD/get_Binance.py
/usr/local/bin/python3 email_send.py
# 執行完成