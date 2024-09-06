import streamlit as st
import requests

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
    else:
        st.error("Failed to download the PDF. Please try again later.")
