import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
import sys
# 從套件中引用模組
from MACD.get_Binance import retreive_Position




from_address = "u8351574@gmail.com"
to_address = "u8351574@gmail.com"


# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg1 = MIMEMultipart('alternative')

#Retreive Current Position 
Current_Pos = retreive_Position()

msg['From'] = from_address
msg1['From'] = from_address
msg['To'] = to_address
msg1['To'] = to_address
# Create the message (CSV).

# Open the file csv and input the content in the loop 
f = open('./Data/trade_details.csv')
content = '<font size="8">ALERT!</font><br>'
content1 = '<font size="8">ALERT!</font><br>'
reader = csv.reader(f)
# read the buy sell data 
buy_sell_data = open('./Signal/buy_sell.txt', 'r')
buy_sell = buy_sell_data.read()
MACD_signal_data = open('./Signal/MACD_Signal.txt', 'r')
MACD_signal = MACD_signal_data.read()


#read the EMA and MACD data
EMA_ALL = open('./Signal/EMA.txt', 'r')
MACD = open('./Signal/MACD.txt', 'r')
MACD_data = MACD.read()
Price = open('./Signal/Price.txt', 'r')
Price_data = Price.read()
Predict_price = open('./Signal/Predict_price.txt', 'r')
Predict_price_data = Predict_price.read()
Predict_sell_price = open('./Signal/Predict_sell_price.txt', 'r')
Predict_sell_price_data = Predict_sell_price.read()

#For EMA strategy
if buy_sell == '0' :
  content += '<font size="6">BUY!<br></font>'
else:
  content += '<font size="6">SELL!<br></font>'

for row in reader:
    content += '<font size="6">'+str(row)+'<br></font>'

for row_ema in EMA_ALL:
    content += '<font size="6">'+'EMA:'+str(row_ema)+'<br></font>'

#For MACD strategy

if MACD_signal == '1' :
  content1 = '<font size="6">Ready to BUY<br></font>'
elif MACD_signal == '2' :
  content1 += '<font size="6">Ready to SELL<br></font>'
elif MACD_signal == '3' :
  content1 += '<font size="6">Warning<br></font>'
elif MACD_signal == '4' :
  content1 += '<font size="6">BUY<br></font>'
elif MACD_signal == '5' :
  content1 += '<font size="6">SELL<br></font>'

if Current_Pos == '0':
    content1 += '<font size="6">Current Position : Sell </font>'
if Current_Pos == '1':
    content1 += '<font size="6">Current Position : Buy </font>'
content1 += '<font size="6">'+'MACD:'+MACD_data+'<br></font>'
content1 += '<font size="6">'+'Price:'+Price_data+'<br></font>'
content1 += '<font size="6">'+'Predict Price:'+Predict_price_data+'<br></font>'
content1 += '<font size="6">'+'Predict Sell Price:'+Predict_sell_price_data+'<br></font>'


content += '<font size="6">Regards Sean</font>'
content1 += '<font size="6">Regards Sean</font>'

part1 = MIMEText(content)
MACD_part1 = MIMEText(content1)

msg['Subject'] = "ETH EMA email"
msg1['Subject'] = "ETH MACD email"

html = """
<html>
  <head></head>
  <body>
    <p>
    <br>"""+content+"""<br>
    </p>
  </body>
</html>
"""

html1 = """
<html>
  <head></head>
  <body>
    <p>
    <br>"""+content1+"""<br>
    </p>
  </body>
</html>
"""
# Record the MIME type - text/html.
part2 = MIMEText(html, 'html')
MACD_part2 = MIMEText(html1, 'html')

#add the file in the mail

#att = MIMEText(open('./Data/binance_ETHUSDT_data.xlsx', 'rb').read(), 'base64', 'utf-8')
#att["Content-Type"] = 'application/octet-stream'
#att["Content-Disposition"] = 'attachment; filename="binance_ETHUSDT_data.xlsx"'

# Attach parts into message container
msg.attach(part1)
msg.attach(part2)
msg1.attach(MACD_part1)
msg1.attach(MACD_part2)
#msg.attach(att)


# Credentials
username = 'u8351574@gmail.com'  
password = 'qknvwdlikvbozwap'  
# Sending the email
## note - this smtp config worked for me, I found it googling around, you may have to tweak the # (587) to get yours to work
server = smtplib.SMTP('smtp.gmail.com', 587) 
server.ehlo()
# if the signal = 1 then send the mail
email_data = open('./Signal/email_send_signal.txt', 'r')
email_signal_temp = email_data.read()




#if email_signal_temp == '1':
#  server.starttls()
#  server.login(username,password)  
#  server.sendmail(from_address, to_address, msg.as_string())  
#  server.quit()
#  email_data = open('./Signal/email_send_signal.txt', 'w')
#  email_data.write('0')
  
  
  
if MACD_signal == '1' or MACD_signal == '2' or MACD_signal == '3' or MACD_signal == '4' or MACD_signal == '5':
  server.starttls()
  server.login(username,password)  
  server.sendmail(from_address, to_address, msg1.as_string())  
  server.quit()
  email_data = open('./Signal/MACD_Signal.txt', 'w')
  email_data.write('0')
