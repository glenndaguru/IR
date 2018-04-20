# Compiled By Mfundo Masango
# Year: 2018

import smtplib
from datetime import datetime


#IP Address For Email Server
SERVER = "192.168.10.21"

#Sender And Recepient(s)
FROM = "alert@coj.co.za"
TO = ["responder1@coj.co.za","responder2@coj.co.za","responder3@coj.co.za","responder4@coj.co.za"]

#Subject Assignment
SUBJECT = "Start Incident Response"

#Message Assignment
TEXT = "Commence incident reponse activity \nDate/Time: "+datetime.now().strftime('%Y-%m-%d% %H:%M:%S')

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
