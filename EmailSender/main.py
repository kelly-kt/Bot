# environment variable library
import os
# import Config
# python email library
import smtplib
# import imghdr
from email.message import EmailMessage

# retrieve sender account info from environment variables
# the sender username and password are installed in replit environment variables

EMAIL_ADDRESS = os.environ['EMAIL_USER']
EMAIL_PASSWORD = os.environ['EMAIL_PASS']

# receiver email address
contacts = ['projectbot@mail.com', 'tepckm@gmail.com',
            'ceedistefano@gmail.com', 'Kellythee01@gmail.com']


# compose emails
msg = EmailMessage()
msg['Subject'] = 'TEP GROUP - TEST'
msg['From'] = EMAIL_ADDRESS
msg['To'] = contacts
msg.set_content(
    'Hello, I am not only discord bot but also a superhero! See the attachment and you will know who I am.')

# email attachment files
files = ['CV_Example.pdf', 'shin.jpg']

for file in files:
    with open(file, 'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype='application',
                       subtype='octet-stream', filename=file_name)

# send emails
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    smtp.send_message(msg)
