# Compiled By Mfundo Masango
# Year: 2017

import smtplib
import argparse
from dateutil import parser

#GLOBAL VARIABLES CAPTURED THROUGH PASSED PARAMETERS
#MACHINE_IP = socket.gethostbyname(socket.gethostname())
SENDER_EMAIL = ""
RECEPIENT_EMAIL = ""
MESSAGE = ""
SUBJECT = ""

def _email(sender,recepient,message,subject):

	#IP Address For Kali Machine
	SERVER = "10.10.10.4"

	#Sender And Recepient(s)
	FROM = sender
	TO = [recepient]

	#Subject Assignment
	SUBJECT = subject

	#Message Assignment
	TEXT = message

	#Joining of All Components
	the_message = """From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

	try:
		#SMTP usage for sending email
		server = smtplib.SMTP(SERVER)
		server.sendmail(FROM, TO, the_message)
		server.quit()

	except OSError:
		print("Error: Email not sent")

if __name__ == '__main__':
	_email(SENDER_EMAIL,RECEPIENT_EMAIL,MESSAGE,SUBJECT)
