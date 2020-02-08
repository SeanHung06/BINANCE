import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv




from_address = "u8351574@gmail.com"
to_address = "u8351574@gmail.com"
# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')

msg['From'] = from_address
msg['To'] = to_address
# Create the message (CSV).

# Open the file csv and input the content in the loop 
f = open('trade_details.csv')
content = '<font size="8">ALERT!</font><br>'
reader = csv.reader(f)
# read the buy sell data 
buy_sell_data = open('buy_sell.txt', 'r')
buy_sell = buy_sell_data.read()
#read the EMA data
EMA_ALL = open('EMA.txt', 'r')

if buy_sell == '0':
  content += '<font size="6">BUY!<br></font>'
else:
  content += '<font size="6">SELL!<br></font>'

for row in reader:
    content += '<font size="6">'+str(row)+'<br></font>'

for row_ema in EMA_ALL:
    content += '<font size="6">'+'EMA:'+str(row_ema)+'<br></font>'


content += '<font size="6">Regards Sean</font>'
part1 = MIMEText(content)
msg['Subject'] = "ETH BUY OR SELL email"
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
# Record the MIME type - text/html.
part2 = MIMEText(html, 'html')

#add the file in the mail

att = MIMEText(open('binance_ETHUSDT_data.xlsx', 'rb').read(), 'base64', 'utf-8')
att["Content-Type"] = 'application/octet-stream'
att["Content-Disposition"] = 'attachment; filename="binance_ETHUSDT_data.xlsx"'

# Attach parts into message container
msg.attach(part1)
msg.attach(part2)
msg.attach(att)


# Credentials
username = 'u8351574@gmail.com'  
password = 'qknvwdlikvbozwap'  
# Sending the email
## note - this smtp config worked for me, I found it googling around, you may have to tweak the # (587) to get yours to work
server = smtplib.SMTP('smtp.gmail.com', 587) 
server.ehlo()
# if the signal = 1 then send the mail
email_data = open('email_send_signal.txt', 'r')

email_signal_temp = email_data.read()

if email_signal_temp == '1':
  server.starttls()
  server.login(username,password)  
  server.sendmail(from_address, to_address, msg.as_string())  
  server.quit()
  email_data = open('email_send_signal.txt', 'w')
  email_data.write('0')
