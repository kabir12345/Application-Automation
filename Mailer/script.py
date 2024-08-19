import os
import smtplib
import yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def load_config(config_file='/Users/kabir/Downloads/jobs/Mailer/gitlab.yaml'):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def send_email(config, recipient_email, recipient_name):
    sender_email = config['sender_email']
    sender_password = os.getenv("GMAIL_PASSWORD")

    if not sender_password:
        raise ValueError("No password provided. Set the GMAIL_PASSWORD environment variable.")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = config['subject']

    # HTML Body
    body = config['email_body'].format(recipient_name=recipient_name)
    message.attach(MIMEText(body, "html"))

    filename = config['attachment_path']
    try:
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
    except FileNotFoundError:
        print(f"File {filename} not found")
        return

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(filename)}")
    message.attach(part)

    try:
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            text = message.as_string()
            server.sendmail(sender_email, recipient_email, text)
            print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def main():
    config = load_config()
    
    for recipient in config['recipients']:
        send_email(config, recipient['email'], recipient['name'])

if __name__ == "__main__":
    main()