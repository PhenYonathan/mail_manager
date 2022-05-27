from django.db import models

# Create your models here.


class GetMails(models.Model):

    variable = "hello"

    # import imaplib
    # import email
    # from email.header import decode_header
    # import webbrowser
    # import os
    #
    # server = "imap.gmail.com"
    # imap = imaplib.IMAP4_SSL(server)
    #
    # username = ""
    # password = ""
    #
    # imap.login(username, password)
    #
    # res, messages = imap.select('"[Gmail]/Sent Mail"')
    #
    # messages = int(messages[0])
    #
    # n = 3
    #
    # for i in range(messages, messages - n, -1):
    #     res, msg = imap.fetch(str(i), "(RFC822)")
    #     for response in msg:
    #         if isinstance(response, tuple):
    #             msg = email.message_from_bytes(response[1])
    #
    #             From = msg["From"]
    #
    #             subject = msg["Subject"]
    #
    #             print("From : ", From)
    #             print("subject : ", subject)

