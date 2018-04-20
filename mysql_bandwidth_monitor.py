#Monitor MySQL Bandwidth use
#Author WA Labuschagne
#Date: 9 April 2018
#Version: 1.0

import glob, os
import time
import sys
import shlex, subprocess
from subprocess import Popen, PIPE
import shutil, errno
import logging
import logging.handlers
import smtplib


#TODO
#Read from database connection details from file
USERNAME = "root"
DATABASE = "employees"
PASSWORD = "playpen2016"

#email server IP
global EMAIL_SERVER
global RECEPIENT

EMAIL_SERVER = "10.0.5.45"
RECEPIENT = ["test2@test.co.za","test3@test.co.za"]

def setDBValues():
	global HOSTNAME
	global USERNAME
	global PASSWORD
	global DATABASE
	global SENSOR_ID
	global LOGGING
	
	try:
		text_file = open("database.txt", "r")
		lines = text_file.read().split(',')
		
		#print(lines)

		HOSTNAME = lines[0]
		USERNAME = lines[1]
		PASSWORD = lines[2]
		DATABASE = lines[3]
		SENSOR_ID = lines[4]
		LOGGING = lines[5]
		
	except Exception as e:
		print("Error: "+str(e))	

#email 
def send_email(Sender,Recepient, Message, Subject):
	
    #Sender And Recepient(s)
    FROM = Sender
    TO = Recepient

    #Subject Assignment
    SUBJECT = Subject

    #Message Assignment
    TEXT = Message

    #Joining of All Components
    message = """\
    From: %s
    To: %s
    Subject: %s
    
    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    #SMTP usage for sending email
    server = smtplib.SMTP(EMAIL_SERVER)
    server.sendmail(FROM, TO, message)
    server.quit()
		
#create a log to rsyslog
def logInfo(message):
	
	logger = logging.getLogger('SensorMySQLLogger')
	logger.setLevel(logging.INFO)

	#add handler to the logger
	handler = logging.handlers.SysLogHandler('/dev/log')

	#add formatter to the handler
	formatter = logging.Formatter('mysql_traffic: { "loggerName":"%(name)s", "asciTime":"%(asctime)s", "pathName":"%(pathname)s", "logRecordCreationTime":"%(created)f", "functionName":"%(funcName)s", "levelNo":"%(levelno)s", "lineNo":"%(lineno)d", "time":"%(msecs)d", "levelName":"%(levelname)s", "message":"%(message)s"}')

	handler.formatter = formatter
	logger.addHandler(handler)

	logger.info(message)

#connect to MYSQL database and determine the bytes sent	
def getMYSQLData(username,database,password):
	#command to connect to database using mysql and extract the data sent
	command_line = "sudo mysql -u "+username+" -p"+password+" -D "+database+" -e 'SHOW GLOBAL STATUS LIKE \"Bytes_sent\"' "
	#print(command_line)
	args = shlex.split(command_line)
	#print(args)
	p = subprocess.Popen(args,stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate()
	#print (stdout)
	myvalues = str(stdout).split("Bytes_sent")
	values = removeSpecial(myvalues[1])
	values = values[1:]
	values = values[:-1]
	#print(values)
	return values

#remove special charaters from string	
def removeSpecial(string):
	return ''.join(e for e in string if e.isalnum())
		
if __name__ == '__main__':
	#wait before start, allows the service to start
	#WAIT_START
	time.sleep(20)
	
	try:
		myNum = 0 
		initial = True 
		old_value = 0 
		new_value = 0
		
		#obtain initial value
		value = int(getMYSQLData(USERNAME,DATABASE,PASSWORD))
		
		#print("Start..."+str(value))

		#Continious scan
		while True:
			time.sleep(5)
			
			new_value2 = 0
			
			if(initial):
				new_value = int(getMYSQLData(USERNAME,DATABASE,PASSWORD))
				difference = new_value - value
				#print("Value1 " +  str(test_value))
				initial = False
				old_value = new_value
				
			else:
				new_value2 = int(getMYSQLData(USERNAME,DATABASE,PASSWORD))
				difference = new_value2 - old_value
				old_value = new_value2
				#print("Value2 " +  str(test_value))
			print_value = difference
			#print("Difference "+str(print_value))
			
			#check that values for Bytes sent
			if(print_value > 10000):
				#print("MySQL: High Data Exfiltration")
				logInfo("MySQL: High Data Exfiltration")
				#Send email
				send_email("test1@test.co.za",RECEPIENT,"MySQL: High Data Exfiltration","Alert (MySQL: High Data Exfiltration)")
				logInfo("MySQL: Email Sent")
				#Add exit
				logInfo("MySQL High Traffic Sensor: Application Exit")
				sys.exit()
	except Exception as e:
		logInfo(str(e))
		print ("Error: " + str(e))		