
import pandas as pd
import json
from datetime import datetime
import os
from nsepython import *
import requests
import time
from email.message import EmailMessage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pdfkit 
import subprocess
import os


holidays2024 = {
    "26-01-2024": "Republic Day",
    "08-03-2024": "Maha Shivaratri",
    "25-03-2024": "Holi",
    "29-03-2024": "Good Friday",
    "11-04-2024": "Eid-Ul-Fitr (Ramzan Eid)",
    "17-04-2024": "Ram Navami",
    "01-05-2024": "Maharashtra Day",
    "20-05-2024": "General Parliamentary Elections",
    "17-06-2024": "Bakri Eid",
    "17-07-2024": "Moharram",
    "15-08-2024": "Independence Day",
    "02-10-2024": "Mahatma Gandhi Jayanti",
    "01-11-2024": "Diwali-Laxmi Pujan",
    "15-11-2024": "Gurunanak Jayanti",
    "25-12-2024": "Christmas",
}

current_date = '17-05-2024'


TelegramBotCredential2 = '6794059157:AAHHpVzTEl-oVNewNbLHJUoe6elTwqm7n5U'

#TelegramBotCredential2 = os.environ.get("TelegramBotCredential2")
#ReceiverTelegramID = os.environ.get("ReceiverTelegramID")

ReceiverTelegramID = '@crontabjob01'

def SendMessageToTelegram(Message):
    try:
        Url = "https://api.telegram.org/bot" + str(TelegramBotCredential2) +  "/sendMessage?chat_id=" + str(ReceiverTelegramID)
        print(Url)
        textdata ={ "text":Message}
        response = requests.request("POST",Url,params=textdata)
    except Exception as e:
        Message = str(e) + ": Exception occur in SendMessageToTelegram"
        print(Message)

def SendTelegramFile(FileName):
    Documentfile={'document':open(FileName,'rb')}
    Fileurl = "https://api.telegram.org/bot" + str(TelegramBotCredential2) +  "/sendDocument?chat_id=" + str(ReceiverTelegramID)
    print(Fileurl)
    response = requests.request("POST",Fileurl,files=Documentfile)




def format_as_crores(x):
    if isinstance(x, float):
        return f"{x / 10000000:.2f} Cr"
    else:
        return x

def security_wise_archive(from_date, to_date, symbol,drop, series="ALL"):
    base_url = "https://www.nseindia.com/api/historical/securityArchives"
    url = f"{base_url}?from={from_date}&to={to_date}&symbol={symbol.upper()}&dataType=priceVolumeDeliverable&series={series.upper()}"
    #print(url)
    p=nsefetch(url)
    df=pd.DataFrame(p['data'])
    selected_columns = ['mTIMESTAMP','CH_SYMBOL','CH_TOT_TRADED_QTY','CH_TOT_TRADED_VAL','COP_DELIV_QTY','COP_DELIV_PERC']
    df[['CH_TOT_TRADED_VAL']] = df[['CH_TOT_TRADED_VAL']].applymap(format_as_crores)

    # Create new DataFrame from selected columns
    new_df = df[selected_columns]
    print(f"Received Drop : {drop}")

"""
    
    if drop:

        #print(new_df)
        #print(new_df.info())
        new_df.rename(columns={c: None for c in df.columns}, inplace=True)
        #print(new_df)
        #new_df.columns = headers
        selected_data = new_df.to_csv(f'{from_date}.csv', mode='a', index=False)

    else:
        selected_data = new_df.to_csv(f'{from_date}.csv', mode='a', index=False, header=headers)
"""
"""
my_list = [
    "Niftybees", "bankbees", "hdfcsensex",
    "nv20ietf", "juniorbees", "monifty500",
    "midcap", "midcapetf", "hdfcsml250",
    "pvtbanietf", "psubnkbees", "bfsi",
    "cpseetf", "icicib22", "autobees",
    "itbees", "tnidetf", "pharmabees",
    "healthy", "infraietf", "makeindia",
    "consumbees", "Commoietf", "Lowvolietf",
    "mom30ietf", "smallcap", "alpha",
    "goldbees", "silverbees", "mon100",
    "masptop50", "mafang", "morealty",
    "ltgiltbees", "esg", "kotakmid50"
]
"""

my_list = [
    "Niftybees","itbees"
]


for counter,i in my_list:
    if counter == 0:
       security_wise_archive('17-05-2024', '17-05-2024', i,drop=False)
    else:
       security_wise_archive('17-05-2024', '17-05-2024', i,drop=True)



#SendTelegramFile('17-05-2024.csv')


"""

import pandas as pd
import pdfkit

df = pd.read_csv('17-05-2024.csv')
html_table = df.to_html()
subprocess.run(['sudo','apt-get', 'install', 'wkhtmltopdf'])
pdfkit.from_string(html_table, 'destination.pdf')
"""

"""




import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Set up the email parameters
sender_email = "tradersbardataupdater@outlook.in"
recipient_email = "dotitebaj.jitavudon@rungel.net"
subject = "CSV Attachment"
password = "TradersBarStockMarket"
filename = "17-05-2024.csv"
"""










import mimetypes

recipient_email = "vamiy71000@mcatag.com"

msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = recipient_email
msg["Subject"] = "help I cannot send an attachment to save my life"
msg.preamble = "help I cannot send an attachment to save my life"


fileToSend = '17-05-2024.csv'

ctype, encoding = mimetypes.guess_type(fileToSend)
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"

maintype, subtype = ctype.split("/", 1)
if maintype == "text":
    fp = open(fileToSend)
    attachment = MIMEText(fp.read(), _subtype=subtype)
    fp.close()
attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
msg.attach(attachment)

server = smtplib.SMTP("smtp-mail.outlook.com", 587)
server.starttls()
server.login(sender_email, password)
print(f"logged in {password}@{sender_email}")
server.sendmail(sender_email, recipient_email, message.as_string())
server.quit()

"""
server = smtplib.SMTP("smtp.gmail.com:587")
server.starttls()
server.login(username,password)
server.sendmail(emailfrom, emailto, msg.as_string())
server.quit()
"""
