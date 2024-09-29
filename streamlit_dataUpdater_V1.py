import streamlit as st
import pandas as pd
from datetime import datetime
import os
from nsepython import nsefetch  # Ensure you have this package installed
import requests

# List of symbols
my_list = [
    "Niftybees", "niftyietf", "setfnif50", "bankbees",
    "bankietf", "hdfcsensex", "nv20ietf", "juniorbees",
    "monifty500", "midcap", "midcapetf", "hdfcsml250",
    "pvtbanietf", "psubnkbees", "bfsi", "cpseetf",
    "icicib22", "autobees", "itbees", "itietf",
    "tnidetf", "pharmabees", "healthy", "infraietf",
    "makeindia", "consumbees", "Commoietf", "Lowvolietf",
    "mom30ietf", "smallcap", "alpha", "goldbees",
    "silverbees", "mon100", "masptop50", "mafang",
    "morealty", "ltgiltbees", "esg", "ALPL30IETF", "oilietf",
    "metalietf", "modefence"
]

# Streamlit app setup
st.title("Data Updater V1.0")

# User input for dates
#from_date = st.date_input("From Date", datetime.today())
#to_date = st.date_input("To Date", datetime.today())

from_date= "26-09-2024"
to_date = "26-09-2024"
# Function to fetch and format data
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

def security_wise_archive(from_date, to_date, symbol, series="ALL"):
    base_url = "https://www.nseindia.com/api/historical/securityArchives"
    url = f"{base_url}?from={from_date}&to={to_date}&symbol={symbol.upper()}&dataType=priceVolumeDeliverable&series={series.upper()}"
    p = nsefetch(url)
    df = pd.DataFrame(p['data'])
    if df.empty:
        return None
    else:
        selected_columns = ['mTIMESTAMP', 'CH_SYMBOL', 'CH_TOT_TRADED_QTY', 'CH_TOT_TRADED_VAL', 'COP_DELIV_QTY', 'COP_DELIV_PERC']
        df[['CH_TOT_TRADED_VAL']] = df[['CH_TOT_TRADED_VAL']].applymap(format_as_crores)
        df[["CH_TOT_TRADED_QTY", "COP_DELIV_QTY"]] = df[["CH_TOT_TRADED_QTY", "COP_DELIV_QTY"]].applymap(format_number)
        new_df = df[selected_columns]
        headers = ['Date', 'Symbol', 'Total Traded Qty', 'Total Traded Value', 'Total Delivery Quantity', 'Delivery Percentage']
        new_df.columns = headers
        return new_df

# Loop through the list and append result to a new list
result_list = []
for symbol in my_list:
    df = security_wise_archive(from_date, to_date, symbol)
    if df is not None:
        result_list.append(df)

# Concatenate the result list into a single dataframe
final_df = pd.concat(result_list, ignore_index=True)

# Display the final dataframe as a table
#st.write(final_df)
st.write(final_df.to_html(escape=False), unsafe_allow_html=True)
