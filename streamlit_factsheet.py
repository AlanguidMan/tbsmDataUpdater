"""
import streamlit as st
import requests
import pandas as pd

# URL of the PDF file
pdf_url = "https://niftyindices.com/Factsheet/ind_nifty50.pdf"

# Function to download the PDF with a custom User-Agent header
def download_pdf(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response

# Streamlit app
st.title("Download Nifty 50 Factsheet")

st.write("Click the button below to download the Nifty 50 Factsheet PDF.")

# Button to download the PDF
if st.button("Download PDF"):
    response = download_pdf(pdf_url)
    
    if response.status_code == 200:
        # Provide a download button for the PDF
        st.download_button(
            label="Download Nifty 50 Factsheet",
            data=response.content,
            file_name="ind_nifty50.pdf",
            mime="application/pdf"
        )
        
        # Display the response headers in a mobile-friendly table
        st.subheader("Response Headers")
        
        # Prepare headers for display
        headers_dict = {
            "Header": ["Date", "Last-Modified", "Content-Length (MB)"],
            "Value": [
                response.headers.get("Date"),
                response.headers.get("Last-Modified"),
                f"{int(response.headers.get('Content-Length', 0)) / (1024 * 1024):.2f} MB"
            ]
        }
        
        # Create a DataFrame for better display
        headers_df = pd.DataFrame(headers_dict)
        
        # Display the DataFrame
        st.dataframe(headers_df, use_container_width=True)
    else:
        st.error("Failed to download the PDF. Please try again later.")
"""


import streamlit as st
import requests

# List of URLs
urls = [
    "https://niftyindices.com/Factsheet/ind_nifty50.pdf",
    "https://niftyindices.com/Factsheet/ind_next50.pdf",
    "https://niftyindices.com/Factsheet/ind_nifty_bank.pdf",
    "https://niftyindices.com/Factsheet/ind_nifty_100.pdf",
    "https://niftyindices.com/Factsheet/ind_nifty_200.pdf",
    "https://niftyindices.com/Factsheet/ind_nifty_500.pdf",
    "https://niftyindices.com/Factsheet/ind_Nifty_Midcap_150.pdf",
    "https://niftyindices.com/Factsheet/ind_nifty_midcap250.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_NiftySmallcap250_MomentumQuality100.pdf",
    "https://niftyindices.com/Factsheet/ind_nifty_midcap50.pdf",
    "https://niftyindices.com/Factsheet/ind_nifty_auto.pdf",
    "https://niftyindices.com/Factsheet/ind_Nifty_CPSE.pdf",
    "https://niftyindices.com/Factsheet/ind_nifty_pharma.pdf",
    "https://niftyindices.com/Factsheet/ind_nifty_it.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_NiftyIndiaDigital.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_NIFTY100_ESG_Index.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_Nifty100_ESG_Sector_Leaders.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_Nifty_FinServ_25_50.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_Nifty_FinancialServicesExBank.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_NiftyMidSmallFinancialSevices.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_NiftyMidSmallHealthCare.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_NiftyMidSmallITAndTelecom.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_Nifty_Alpha30.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_Nifty_Finance.pdf",
    "https://niftyindices.com/Factsheet/ind_nifty_smallcap50.pdf",
    "https://niftyindices.com/Factsheet/ind_nifty_fmcg.pdf",
    "https://niftyindices.com/Factsheet/ind_nifty_private_bank.pdf",
    "https://niftyindices.com/Factsheet/ind_nifty_psu_bank.pdf",
    "https://niftyindices.com/Factsheet/ind_nifty_realty.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_nifty_consumer_durables.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_nifty_oil_and_gas.pdf",
    "https://niftyindices.com/Factsheet/ind_nifty_commodities.pdf",
    "https://niftyindices.com/Factsheet/ind_Nifty_India_Consumption.pdf",
    "https://niftyindices.com/Factsheet/ind_nifty_infra.pdf",
    "https://niftyindices.com/Factsheet/FactSheet_Nifty_India_Manufacturing_Index.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_Nifty100_ESG_Sector_Leaders.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_Nifty_Alpha50.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_Nifty_Low_Volatility30.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_Nifty_Alpha_Low-Volatility_30.pdf",
    "https://niftyindices.com/Factsheet/Factsheet_Nifty200_Momentum30.pdf"
]

st.title("URL Status Checker")

selected_url_name = st.selectbox("Select a URL:", url_names)

# Find the corresponding URL
selected_url = urls[url_names.index(selected_url_name)]

# Dropdown menu for URLs
#selected_url = st.selectbox("Select a URL:", urls)

# Button to check status
if st.button("Check Status"):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(selected_url, headers=headers)
        
        last_modified = response.headers.get("Last-Modified", "Not available")
        content_length = response.headers.get("Content-Length", "0")
        
        st.write("Last Modified:", last_modified)
        st.write("Content Length:", content_length)

        # Provide a download link if the content length is greater than 0
        if int(content_length) > 0:
            st.markdown(f"[Download File]({selected_url})", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error checking the URL: {e}")
        
