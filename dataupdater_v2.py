print("starting DataUpdater V2.o...")

import pandas as pd
import mimetypes
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

#current_date = datetime.datetime.now().strftime("%d-%m-%Y")
current_date = "24-04-2024"
print(current_date)
csvfile= f'{current_date}.csv'
pdffile= f'{current_date}.pdf'
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

def format_number(amount):
    if amount >= 10000000:
        return f"{amount / 10000000:.2f} crore"
    elif amount >= 100000:
        return f"{amount / 100000:.2f} lakh"
    else:
        return f"{amount / 1000:.2f} thousand"

def format_as_crores(x):
    if isinstance(x, float):
        return f"{x / 10000000:.2f} Cr"
    else:
        return x

def mailSend():
    start_time = time.time()
    sender_email = "tradersbardataupdater@outlook.in"
    recipient_email = "dotitebaj.jitavudon@rungel.net"
    subject = f"Delivery position for {current_date} "
    password = "TradersBarStockMarket"
    recipient_email = "vamiy71000@mcatag.com"
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.preamble = subject
    f= open(csvfile)
    attachment = MIMEText(f.read(), _subtype="csv")
    f.close
    attachment.add_header("Content-Disposition", "attachment", filename=f"{csvfile}")
    msg.attach(attachment)
    with open(pdffile, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype="pdf")
        attachment.add_header('Content-Disposition','attachment',filename=f"{pdffile}")
        msg.attach(attachment)
    server = smtplib.SMTP("smtp-mail.outlook.com", 587)
    server.starttls()
    server.login(sender_email, password)
    print(f"logged in {password}@{sender_email}")
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()
    end_time = time.time()
    exim = end_time - start_time
    print("email sent in: ", exim)
    

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
    "ltgiltbees", "esg"
]

def security_wise_archive(from_date, to_date, symbol, drop, series="ALL"):
    base_url = "https://www.nseindia.com/api/historical/securityArchives"
    url = f"{base_url}?from={from_date}&to={to_date}&symbol={symbol.upper()}&dataType=priceVolumeDeliverable&series={series.upper()}"
    #print(url)
    p = nsefetch(url)
    df = pd.DataFrame(p['data'])
    if df.empty:
        return None
    else:
        #return f"received data for {symbol}."
        selected_columns = ['mTIMESTAMP','CH_SYMBOL','CH_TOT_TRADED_QTY','CH_TOT_TRADED_VAL','COP_DELIV_QTY','COP_DELIV_PERC']
        df[['CH_TOT_TRADED_VAL']] = df[['CH_TOT_TRADED_VAL']].applymap(format_as_crores)
        df[["CH_TOT_TRADED_QTY", "COP_DELIV_QTY"]] = df[["CH_TOT_TRADED_QTY", "COP_DELIV_QTY"]].applymap(format_number)
        # Create new DataFrame from selected columns
        new_df = df[selected_columns]
        headers = ['Date', 'Symbol', 'Total Traded Qty', 'Total Traded Value', 'Total Delivery Quantity', 'Delivery Percentage']
        new_df.columns = headers
        return(new_df)

"""
    # Write to CSV file in append mode
    if drop:
        new_df.to_csv(f'{from_date}.csv', mode='a', header=False, index=False)
    else:
        new_df.to_csv(f'{from_date}.csv', mode='a', header=headers, index=False)
#rdx= security_wise_archive(current_date,current_date,"silverbees",drop = False)
#rdx.loc[0] = ['17-05-2024', 'Bankbees', 1000, 200000, 800, 80]
dfx = security_wise_archive(current_date,current_date,"itbees",drop = False)
print("Dfx :", dfx.info())
print("Rdx :", rdx.info())
result= pd.concat([rdx, dfx], ignore_index=True)
print("cancating rdx to dfx ")
print(result)
"""
start_time = time.time()
startime = start_time
rdx = pd.DataFrame()

for i in my_list:
    dfx= security_wise_archive(current_date,current_date,i,drop = False)
    if dfx is None:
        break
    else:
        rdx = pd.concat([rdx, dfx], ignore_index=False)

if not rdx.empty:
    rdx.to_csv(f"{current_date}.csv")
    html_table = rdx.to_html()
    subprocess.run(['sudo','apt-get', 'install', 'wkhtmltopdf'])
    pdfkit.from_string(html_table, f'{current_date}.pdf')
    end_time = time.time()
    exe_time = end_time - start_time
    print("Data fetched and converted in: ", exe_time)
    mailSend()
    SendTelegramFile(csvfile)
    SendTelegramFile(pdffile)
    final_end_time = time.time()
    totime = final_end_time-startime
    print("Code executed in:", totime)
    SendMessageToTelegram(f"Execution time: {totime} seconds")



"""
for counter,i in enumerate(my_list):
    if counter == 0:
       security_wise_archive(current_date,current_date,i,drop=False)
    else:
       security_wise_archive(current_date, current_date,i,drop=True)

#Multi threading

import concurrent.futures
import time

start_time = time.time()
rdx = pd.DataFrame()
def process_element(i):
    dfx = security_wise_archive(current_date, current_date, i, drop=False)
    if not dfx.empty:
        return dfx
    else:
        print(f"DataFrame {i} is empty")
        return None

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_element, i) for i in my_list]
    for future in concurrent.futures.as_completed(futures):
        dfx = future.result()
        if dfx is not None:
            rdx = pd.concat([rdx, dfx], ignore_index=False)

print(rdx)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
"""
