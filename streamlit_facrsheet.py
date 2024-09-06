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
    return response.content

# Streamlit app
st.title("Download Nifty 50 Factsheet")

st.write("Click the button below to download the Nifty 50 Factsheet PDF.")

# Button to download the PDF
if st.button("Download PDF"):
    pdf_data = download_pdf(pdf_url)
    
    # Save the PDF data to a file
    with open("ind_nifty50.pdf", "wb") as f:
        f.write(pdf_data)
    
    # Provide a link to download the file
    st.success("PDF downloaded successfully!")
    st.markdown("[Click here to download the Nifty 50 Factsheet](ind_nifty50.pdf)", unsafe_allow_html=True)
