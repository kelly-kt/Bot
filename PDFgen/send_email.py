import Config

import smtplib
# import imghdr
from email.message import EmailMessage


def send_report(pdf_file):
    print("Sending generated email report to",
          Config.config['email']['receivers'])

    # compose emails
    msg = EmailMessage()
    msg['Subject'] = 'Report -- Disbot Team'
    msg['From'] = Config.config['email']['username']
    msg['To'] = Config.config['email']['receivers']
    msg.set_content('Hello, The report is attached. -- Disbot Team')

    with open(pdf_file, 'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype='application',
                       subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Config.config['email']['username'],
                   Config.config['email']['password'])

        smtp.send_message(msg)
