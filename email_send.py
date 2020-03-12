import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv




from_address = "u8351574@gmail.com"
to_address = "u8351574@gmail.com"


# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg1 = MIMEMultipart('alternative')

msg['From'] = from_address
msg1['From'] = from_address
msg['To'] = to_address
msg1['To'] = to_address
# Create the message (CSV).

# Open the file csv and input the content in the loop 
f = open('trade_details.csv')
content = '<font size="8">ALERT!</font><br>'
content1 = '<font size="8">ALERT!</font><br>'
reader = csv.reader(f)
# read the buy sell data 
buy_sell_data = open('buy_sell.txt', 'r')
buy_sell = buy_sell_data.read()
MACD_signal_data = open('./MACD_Signal.txt', 'r')
MACD_signal = MACD_signal_data.read()


#read the EMA and MACD data
EMA_ALL = open('EMA.txt', 'r')
MACD = open('./MACD.txt', 'r')
MACD_data = MACD.read()

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
  content1 += '<font size="6">BUY!<br></font>'
elif MACD_signal == '2' :
  content1 += '<font size="6">SELL!<br></font>'

content1 += '<font size="6">'+'MACD:'+MACD_data+'<br></font>'


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

att = MIMEText(open('binance_ETHUSDT_data.xlsx', 'rb').read(), 'base64', 'utf-8')
att["Content-Type"] = 'application/octet-stream'
att["Content-Disposition"] = 'attachment; filename="binance_ETHUSDT_data.xlsx"'

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
email_data = open('email_send_signal.txt', 'r')
MACD_data = open('./MACD_Signal.txt', 'r')
email_signal_temp = email_data.read()
email_signal_temp2 = MACD_data.read()




if email_signal_temp == '1':
  server.starttls()
  server.login(username,password)  
  server.sendmail(from_address, to_address, msg.as_string())  
  server.quit()
  email_data = open('email_send_signal.txt', 'w')
  email_data.write('0')
  
  
  
  
if email_signal_temp2 == '1' or email_signal_temp2 == '2':
  server.starttls()
  server.login(username,password)  
  server.sendmail(from_address, to_address, msg1.as_string())  
  server.quit()
  email_data = open('./MACD_Signal.txt', 'w')
  email_data.write('0')
