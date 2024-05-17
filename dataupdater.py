import pandas as pd
import json
from datetime import datetime
import os
from nsepython import nsefetch
import requests
import time
from email.message import EmailMessage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pdfkit 
#import subprocess
import os



def security_wise_archive(from_date, to_date, symbol, series="ALL"):
    base_url = "https://www.nseindia.com/api/historical/securityArchives"
    url = f"{base_url}?from={from_date}&to={to_date}&symbol={symbol.upper()}&dataType=priceVolumeDeliverable&series={series.upper()}"
    #print("starting to fetch data ")
    print(url)
    p=nsefetch(url)
    #print(type(p))
    #print("received data1")
    df=pd.DataFrame(p['data'])
    selected_columns = ['mTIMESTAMP','CH_SYMBOL','CH_TOT_TRADED_QTY','CH_TOT_TRADED_VAL','COP_DELIV_QTY','COP_DELIV_PERC']
    selected_data = df.loc[:, selected_columns].to_html()
    return selected_data

    #selected_data = json.dumps(selected_data.to_dict('records'))
    #return(selected_data)



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


html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Delivery data for {current_date}</title>
<style > body{font-family:Arial, sans-serif;margin:0;padding:0;background-color:#f2f2f2;color:#333333}.container{max-width:600px;margin:auto;padding:20px;background-color:#ffffff;border-radius:10px;overflow:hidden;text-align:center}h1{text-align:center;color:#333333}p{margin-bottom:20px;font-size:18px}.cta-button{display:block;width:30%;text-align:center;background-color:#333333;color:#ffffff;text-decoration:none;margin:0 auto;padding:8px 0;border-radius:5px}.logo{display:block;margin:auto;width:150px;border-radius:50%;margin-bottom:20px}@media only screen and (max-width: 600px){.container{padding:10px}}</style>
</head>
<body>
<div class="container">
    <img src="https://cloudsconvert.com/dl.php?token=+ixZ6aLy08arfdsQfaMQ81e5KRg09ec9hhjPznNfVxo8WD5aHxwL5MJ1SWc8pK/CSl3o3o6H6+5QJjHqhT4Ynr8astT89NszeYNha/EtXC8lsdB+EkiQKQUxekoaYVBXRehnSb2FW08arq6ij88zcLaqNAMXo+f6UKWIbkXqr9rPYtHWxvMmGorEeEPqoY9m1K433RuhlH5qNG6isfzBpt4s2iW5xcj5ikYy/HD57cEuUVeQDQ==" alt="Logo" class="logo">
    <h1>Good Evening, sir.</h1>
    <p>Please find the below file. It contains delivery positions for different ETFs for {current_date}.</p>
    <p>After downloading the file, open it in Chrome. Thank you 😊 🙏.</p>
    <a href="#" class="cta-button">Download File</a>
</div>
</body>
</html>
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

current_date = datetime.now().strftime("%d-%m-%Y")
print(current_date)
#current_date= '16-05-2024'
output_file_name=f"{current_date}.html"


if current_date in holidays2024:
    SendMessageToTelegram(f"Wishing you a happy {holidays2024[current_date]}!")
else:
    with open(output_file_name, 'a') as file:
        start_time = time.time()
        for symbol in my_list:  # Assuming list is defined somewhere in your code
            print(f"running {symbol.upper()}")
            data = security_wise_archive(current_date, current_date, symbol)
            file.write(f"\n{data}\n\n")
        file.close()
    SendMessageToTelegram("Sending file...")
    print("sending file to Telegram")
    SendTelegramFile(f"{current_date}.html")
    print("successfully sent file")
    end_time = time.time()
    execution_time = end_time - start_time
    SendMessageToTelegram(f"The code took {execution_time} seconds to complete.")
    
    sender = os.environ.get("EMAIL_SENDER")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    recipient = os.environ.get("EMAIL_RECIPIENT")
    message = "Good Evening, sir. please find the below file. It contains delivery positions for different ETFs. After downloading the file, open it in Chrome. Thank you 😊 🙏 "

    #email = EmailMessage()
    email= MIMEMultipart('related')
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = f"Delivery position for {current_date}"
    #email.set_content(message)
    email.attach(MIMEText(html_content, 'html'))
    #subprocess.run(['sudo','apt-get', 'install', 'wkhtmltopdf'])
    pdfkit.from_file(f"{current_date}.html", f'{current_date}.pdf')
    with open(f"{current_date}.html", 'rb') as f, open(f'{current_date}.pdf', 'rb') as f2:
        file_data = f.read()
        file2_data = f2.read()
    email.add_attachment(file_data, maintype='text', subtype='html', filename=f"{current_date}.html")
    email.add_attachment(file2_data, maintype='application', subtype='pdf', filename=f'{current_date}.pdf')
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(sender, EMAIL_PASSWORD)
    print("logged in successfully")
    SendMessageToTelegram(f"sending mail to {recipient}")
    smtp.sendmail(sender, recipient, email.as_string())
    smtp.quit()
    SendTelegramFile(f"{current_date}.pdf")
    print("email sent")
