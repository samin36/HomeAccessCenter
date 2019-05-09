## https://www.youtube.com/watch?v=JRCJ6RtE3xU ##

import os
import smtplib
from email.message import EmailMessage

SENDER_EMAIL = os.environ.get('PYTHON_PROJECTS_USERNAME')
SENDER_PASSWORD = os.environ.get('PYTHON_PROJECTS_PASSWORD')


class EmailAlert(object):
    def __init__(self, receiver, subject, message):
        self.msg_creator = EmailMessage()
        self.msg_creator['Subject'] = subject
        self.msg_creator['From'] = SENDER_EMAIL
        self.msg_creator['To'] = receiver
        self.msg_creator.set_content(message)

    def send_email(self, attachment=None):
        if attachment is not None:
            with open(attachment, 'rb') as file:
                file_data = file.read()
                file_name = file.name
            self.msg_creator.add_attachment(file_data, maintype='application',
                                            subtype='octet-stream', filename=file_name)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(self.msg_creator)
            print("Email sent successfully")
            return True
