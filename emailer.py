import os
import smtplib
from email.message import EmailMessage
import requests as r 


def send_email(file_path):
    msg = EmailMessage()
    msg['Subject'] = "sending the first file"
    msg['From'] = "tradersbardataupdater@outlook.in"
    msg['To'] = "papoye8837@nweal.com"

    with open(file_path, 'rb') as file:
        file_data = file.read()
        file_name = os.path.basename(file_path)
    
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(msg)

# URL of the image to download from NASA
image_url = "https://images-assets.nasa.gov/image/PIA03606/PIA03606~large.jpg?w=1024&h=1024&fit=crop&crop=faces%2Cfocalpoint"


# Send a GET request to the image URL
response = requests.get(image_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Open a file in binary write mode to save the image
    with open("nasaimage.jpg", "wb") as f:
        # Write the content of the response to the file
        f.write(response.content)
    print("Image downloaded and saved successfully.")
    if "nasaimage.jpg" in os.listdir():
        send_email("nasaimage.jpg")
    else:
        print("can't find file")
else:
    print("Failed to download the image.")
    
