# Compiled By Mfundo Masango
# Year: 2018

import smtplib
import argparse
from dateutil import parser

#IP Address For Kali Machine
SERVER = "10.0.5.45"

#Capture Arguments From Terminal (Sender,Recepient, Message and Subject)
parse = argparse.ArgumentParser()
parse.add_argument("sender",help="Enter sender email")
parse.add_argument("recepient",help="Enter recepient(s) email")
parse.add_argument("message",help="Enter message")
parse.add_argument("subject",help="Enter Subject")
args = parse.parse_args()

#Sender And Recepient(s)
FROM = args.sender
TO = [args.recepient]

#Subject Assignment
SUBJECT = args.subject

#Message Assignment
TEXT = args.message

#Joining of All Components
message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

#SMTP usage for sending email
server = smtplib.SMTP(SERVER)
server.sendmail(FROM, TO, message)
server.quit()
