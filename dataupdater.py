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

list = ["nv20ietf","Niftybees","bankbees",
        "psubnkbees","bfsi","pvtbanietf",
        "juniorbees","midcapetf","hdfcsml250",
        "sensexietf","cpseetf","icicib22","mon100",
        "mom30ietf","mafang","itbees","pharmabees","kotakalpha",
        "consumbees","makeindia","infraietf","infrabees",
        "autobees","goldbees","silverbees","ltgiltbees",
        "Commoietf","healthy","tnidetf","masptop50",
        "Lowvolietf","monifty500","kotakmid50"]

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




def send_email(sender_email, sender_password, receiver_email, subject, body= None, attachment_path=None):
    msg = MIMEMultipart();msg['From']=sender_email;msg['To']=receiver_email;msg['Subject']=subject
    msg.attach(MIMEText(body,'plain'))
    if attachment_path:
        filename=attachment_path;attachment=open(filename,"rb")
        part=MIMEBase('application','octet-stream');part.set_payload((attachment).read());encoders.encode_base64(part)
        part.add_header('Content-Disposition',"attachment; filename= %s"%filename);msg.attach(part)
    try:
        server=smtplib.SMTP('smtp-mail.outlook.com',587);server.starttls();server.login(sender_email,sender_password)
        server.sendmail(sender_email,receiver_email,msg.as_string());server.quit()
    except smtplib.SMTPAuthenticationError:
        print("Failed to login to SMTP server. Check email and password.")



sender_email = 'tradersbardataupdater@outlook.in'
sender_password = 'TradersBarStockMarket'
receiver_email = 'papoye8837@nweal.com'
body =None
current_date = datetime.now().strftime("%d-%m-%Y")
print(current_date)
current_date= '16-05-2024'
subject= f"Delivery position for {current_date}"
output_file_name=f"{current_date}.html"
attachment_file = output_file_name



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
    print("Sent message")
    print("sending email")
    send_email(sender_email, sender_password, receiver_email, subject, body, attachment_path=attachment_file)
    print("email sent")


