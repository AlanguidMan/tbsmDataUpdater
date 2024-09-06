import streamlit as st
import requests

# URL of the PDF file
pdf_url = "https://niftyindices.com/Factsheet/ind_nifty50.pdf"

# Function to download the PDF
def download_pdf(url):
    response = requests.get(url)
    return response.content

# Streamlit app
st.title("Download Nifty 50 Factsheet")

st.write("Click the button below to download the Nifty 50 Factsheet PDF.")

# Button to download the PDF
if st.button("Download PDF"):
    pdf_data = download_pdf(pdf_url)
    st.download_button(
        label="Download Nifty 50 Factsheet",
        data=pdf_data,
        file_name="ind_nifty50.pdf",
        mime="application/pdf"
    )
  
