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


def format_as_crores(x):
    if isinstance(x, float):
        return f"{x / 10000000:.2f} Cr"
    else:
        return x

def security_wise_archive(from_date, to_date, symbol, series="ALL"):
    base_url = "https://www.nseindia.com/api/historical/securityArchives"
    url = f"{base_url}?from={from_date}&to={to_date}&symbol={symbol.upper()}&dataType=priceVolumeDeliverable&series={series.upper()}"
    #print(url)
    p=nsefetch(url)
    df=pd.DataFrame(p['data'])
    selected_columns = ['mTIMESTAMP','CH_SYMBOL','CH_TOT_TRADED_QTY','CH_TOT_TRADED_VAL','COP_DELIV_QTY','COP_DELIV_PERC']
    df[['CH_TOT_TRADED_VAL']] = df[['CH_TOT_TRADED_VAL']].applymap(format_as_crores)

    # Create new DataFrame from selected columns
    new_df = df[selected_columns]

    # Change headers
    headers = ['Date', 'Symbol', 'Total Traded Qty', 'Total Traded Value', 'Total Delivery Quantity', 'Delivery Percentage']
    new_df.columns = headers

    selected_data = new_df.to_csv(f'{from_date}.csv', index=False, header=headers)

    print("printing selected data")
    print(selected_data)



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

for i in my_list:
    security_wise_archive('17-05-2024', '17-05-2024', i)