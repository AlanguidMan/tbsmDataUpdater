import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email(sender_email, sender_password, receiver_email, subject, body, attachment_path=None):
    logger.info("Creating email message...")
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add body to email
    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        # Open the file to be sent
        logger.info("Attaching file...")
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
    logger.info("Connecting to SMTP server...")
    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()

        # Login to email account
        logger.info("Logging in to email account...")
        server.login(sender_email, sender_password)

        # Send email
        logger.info("Sending email...")
        server.sendmail(sender_email, receiver_email, msg.as_string())

        # Quit SMTP server
        logger.info("Closing SMTP server connection...")
        server.quit()
    except smtplib.SMTPAuthenticationError:
        logger.critical("Failed to login to SMTP server. Check email and password.")

