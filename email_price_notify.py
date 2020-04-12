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
f = open('./Data/trade_details.csv')
f_1 = open('./Data/binance_ETHUSDT_data.csv')
content = '<font size="4">The price for now is</font><br>'

reader = csv.reader(f)
reader_f1 = csv.reader(f_1)

#read the data
EMA_ALL = open('./Signal/EMA.txt', 'r')
MACD = open('./Signal/MACD.txt', 'r')
MACD_data = MACD.read()
Predict_price = open('./Signal/Predict_price.txt', 'r')
Predict_price_data = Predict_price.read()

for row in reader:
    content += '<font size="6">'+str(row)+'<br></font>'
line_1 = 0
for row_f1 in reader_f1:
    line_1 = line_1 + 1
    

for row_ema in EMA_ALL:
    content += '<font size="6">'+'EMA:'+str(row_ema)+'<br></font>'
content += '<font size="6">'+'MACD:'+MACD_data+'<br></font>'
content += '<font size="6">'+'Predict Price:'+Predict_price_data+'<br></font>'
content += '<font size="6">Regards Sean</font>'
part1 = MIMEText(content)

msg['Subject'] = "ETH Price Notify email"
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

att = MIMEText(open('./Data/binance_ETHUSDT_data.xlsx', 'rb').read(), 'base64', 'utf-8')
att["Content-Type"] = 'application/octet-stream'
att["Content-Disposition"] = 'attachment; filename="binance_ETHUSDT_data.xlsx"'


# Attach parts into message container
msg.attach(part1)
msg.attach(part2)
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

server.starttls()
server.login(username,password)  
server.sendmail(from_address, to_address, msg.as_string())  
server.quit() 


