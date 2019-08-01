## https://www.youtube.com/watch?v=JRCJ6RtE3xU ##

import os
import smtplib
import imghdr
from email.message import EmailMessage

SENDER_EMAIL = username
SENDER_PASSWORD = password


class EmailAlert():
    def __init__(self, receiver, subject, message):
        """
        intializes the email message with subject, from, to, and the message
        itself. Uses the EmailMessage module from email.message
        """
        self.msg_creator = EmailMessage()
        self.msg_creator['Subject'] = subject
        self.msg_creator['From'] = SENDER_EMAIL
        self.msg_creator['To'] = receiver
        self.msg_creator.set_content(message)

    def send_email(self, attachment=None):
        """
        function which sends the email. If an attachment is passed in, and it
        is not a list of names of images, then it is assumed that a pdf file is
        passed in and is sent. Otherwise, it is assumed that a list of image
        file names in the current working directory are passed in.
        """
        if attachment is not None and not isinstance(attachment, list):
            with open(attachment, 'rb') as file:
                file_data = file.read()
                file_name = file.name
            self.msg_creator.add_attachment(file_data, maintype='application',
                                            subtype='octet-stream', filename=file_name)
        else:
            for grade_images in attachment:
                with open(grade_images, 'rb') as file:
                    file_data = file.read()
                    file_name = file.name
                    file_type = imghdr.what(file_name)
                self.msg_creator.add_attachment(file_data, maintype='image',
                                                subtype=file_type, filename=file_name)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(self.msg_creator)
            print("Email sent successfully")
            return True
