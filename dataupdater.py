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


def security_wise_archive(from_date, to_date, symbol, series="ALL"):
    base_url = "https://www.nseindia.com/api/historical/securityArchives"
    url = f"{base_url}?from={from_date}&to={to_date}&symbol={symbol.upper()}&dataType=priceVolumeDeliverable&series={series.upper()}"
    #print("starting to fetch data ")
    #print(url)
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
    "17-06-2024": "Bakri Eid",
    "17-07-2024": "Moharram",
    "15-08-2024": "Independence Day",
    "02-10-2024": "Mahatma Gandhi Jayanti",
    "01-11-2024": "Diwali-Laxmi Pujan",
    "15-11-2024": "Gurunanak Jayanti",
    "25-12-2024": "Christmas",
}


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

#TelegramBotCredential = '5747611163:AAFqIPOxRGTXP25py8mNdXRL7mz-TfsouO8'
TelegramBotCredential = '6883565174:AAGXuW07FEidJ3o8sNNbDTQZ0OpS9WacHj4'
TelegramBotCredential2 = '6794059157:AAHHpVzTEl-oVNewNbLHJUoe6elTwqm7n5U'

#my personal id
ReceiverTelegramID = '@crontabjob01'
ReceiverTelegramID2 = '@tbsmdeldata_bot'

def SendMessageToTelegram(Message):
    try:
        Url = "https://api.telegram.org/bot" + str(TelegramBotCredential2) +  "/sendMessage?chat_id=" + str(ReceiverTelegramID)
        textdata ={ "text":Message}
        response = requests.request("POST",Url,params=textdata)
    except Exception as e:
        Message = str(e) + ": Exception occur in SendMessageToTelegram"
        print(Message)

def SendTelegramFile(FileName):
    Documentfile={'document':open(FileName,'rb')}
    Fileurl = "https://api.telegram.org/bot" + str(TelegramBotCredential2) +  "/sendDocument?chat_id=" + str(ReceiverTelegramID)
    response = requests.request("POST",Fileurl,files=Documentfile)


def send_email(sender_email, sender_password, receiver_email, subject, body, attachment_path=None):
    print("Creating email message...")
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add body to email
    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        # Open the file to be sent
        print(f"Received {attachment_path} as attachment")
        print("Attaching file...")
        filename = attachment_path
        attachment = open(filename, "rb")

        # Add attachment to message
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        # Attach the attachment to the email
        msg.attach(part)

    # Connect to SMTP server
    print("Connecting to SMTP server...")
    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()

        # Login to email account
        print("Logging in to email account...")
        server.login(sender_email, sender_password)
        print(f"logged in successfully {sender_password}@{sender_email}")

        # Send email
        print("Sending email...")
        print(f"Sending to -----> {receiver_email} from {sender_email}")
        
        server.sendmail(sender_email, receiver_email, msg.as_string())

        # Quit SMTP server
        print("Closing SMTP server connection...")
        server.quit()
    except smtplib.SMTPAuthenticationError:
        print("Failed to login to SMTP server. Check email and password.")
        
"""
sender_email = 'tradersbardataupdater@outlook.in'
sender_password = 'TradersBarStockMarket'
receiver_email = 'papoye8837@nweal.com'
body =None
"""
current_date = datetime.now().strftime("%d-%m-%Y")
print(current_date)
current_date= '16-05-2024'
output_file_name=f"{current_date}.html"



if current_date in holidays2024:
    SendMessageToTelegram(f"Wishing you a happy {holidays2024[current_date]}!")
else:
    with open(output_file_name, 'a') as file:
        start_time = time.time()
        for symbol in list:  # Assuming list is defined somewhere in your code
            print(f"running {symbol.upper()}")
            
            data = security_wise_archive(current_date, current_date, symbol)
            file.write(f"\n{data}\n\n")
        file.close()
    SendMessageToTelegram("Sending file...")
    SendTelegramFile(f"{current_date}.html")
    end_time = time.time()
    execution_time = end_time - start_time
    SendMessageToTelegram(f"The code took {execution_time} seconds to complete.")
    sender = "tradersbardataupdater@outlook.in"
    recipient = "papoye8837@nweal.com"
    message = "Hello world!"

    email = EmailMessage()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = f"Delivery position for {current_date}"
    email.set_content(message)

    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(sender, "TradersBarStockMarket")
    print("logged in successfully")
    smtp.sendmail(sender, recipient, email.as_string())
    smtp.quit()
    print("email sent")
