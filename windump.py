import sys
import subprocess
import MySQLdb as db

#Change directory
#cd /d D:

#Method to start TCP DUMP on Start UP
def start_dump(path_to_exe,interface,path_to_file):
	try:
		command = "{} -i {} -C 10 -w {}".format(path_to_exe,interface,path_to_file)
		line = command.split(" ")
		the_process = subprocess.Popen(line,shell=False)
		the_process.communicate()
		
	except Exception as e:
		print(e)
		
def db_query():
	HOST = "10.0.5.33"
	PORT = 3306
	USER = "myuser"
	PASSWORD = "1234"
	DB = "ir_db"

	try:
		connection = db.Connection(host=HOST, port=PORT,user=USER, passwd=PASSWORD, db=DB)
		dbhandler = connection.cursor()
		dbhandler.execute("SELECT * from action")
		result = dbhandler.fetchall()
		for item in result:
			print (item)

	except Exception as e:
		print (e)

	finally:
		connection.close()
		

if __name__ == '__main__':
	path_to_exe = "C:\\Users\\CWRGSTUDENT\\Downloads\\WinDump.exe"
	interface =  "\\Device\\NPF_{C70F18F5-9C91-4F74-8109-E9261DE29B2C}"
	path_to_file = "C:\\Users\\CWRGSTUDENT\\Documents\\windump.pcap"
	start_dump(path_to_exe,interface,path_to_file)
	#db_query()