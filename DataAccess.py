import pymysql
import re
import random
import logging as log

log.basicConfig(filename='dataAccess.log',level=log.DEBUG)

class repetition_checker():
    def __init__(self):
        self.old_val=0

    def check(self,value):
        if self.old_val==value:
            self.old_val=value
            return True
        return False

rep=repetition_checker()


class DataAccess():
    def __init__(self):
        self.mysql_connection = self.get_mysql_connection()

    def get_mysql_connection(db_file): #mysql db connection
        '''
        Opens a new connection to the database, and returns the connection object to the caller.
        '''
        connection = None
        try:
            # get database configuration from database.txt
            '''text_file = open("database.txt", "r")
            lines = re.split(',', text_file.read())
            hostname = lines[0]
            username = lines[1]
            password = lines[2]
            database = lines[3]#'127.0.0.1'
            #connection = pymysql.connect(host=hostname, user=username, password=password, database=database, cursorclass=pymysql.cursors.DictCursor)
            '''
            connection = pymysql.connect(host='10.0.5.30', user='myuser', password='1234', database='ir_db',cursorclass=pymysql.cursors.DictCursor)
            #connection = pymysql.connect(host='192.168.8.126', user='myuser', password='1234', database='ir_db',cursorclass=pymysql.cursors.DictCursor)#host=146.64.182.136
            print('connected')
        except Exception as e:
            print("Error: Could not connect to the database.\n")
            print("Checka di Settings.\n")
            print(str(e))
            log.exception(e)
            exit()
        return connection

    def get_service(self,service_id):
        try:
            sql='SELECT s.service_id,s.service_name FROM service s '
            sql+="WHERE s.service_id="+str(service_id)
            sql+=" AND s.service_id != 3"
            #result=self.query_exec(sql)
            connection = self.mysql_connection

            with connection as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()

        except Exception as e:
            print(str(e))
            log.exception(e)
            
        return result

    def get_servers(self,service_id):
        try:
            sql='SELECT s.server_id,s.server_name,s.ip_addr,s.username,s.password '
            sql+="FROM servers s WHERE s.service="+str(service_id)
            #result=self.query_exec(sql)
            connection = self.mysql_connection

            with connection as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                
        except Exception as e:
            print(str(e))
            log.exception(e)
        return result

    def get_action(self,service_id):
        try:
            sql='SELECT a.action_id, a.method FROM action a '
            #sql+='INNER JOIN service s ON '
            #sql +='s.service_id=a.service '
            sql+="WHERE a.service="+str(service_id)

            connection = self.mysql_connection

            with connection as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()

        except Exception as e:
            print (str(e))
            log.exception(e)

        return result

    def get_ftp_users(self):
        try:
            sql='SELECT user_id,username,password '
            sql+="FROM ftp_users"
            #result=self.query_exec(sql)
            connection = self.mysql_connection

            with connection as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()

        except Exception as e:
            print(str(e))
            log.exception(e)
        return result

class attacker():
    def __init__(self):
        self.data=DataAccess()
        #self.temp_service_id=self.get_service()
        self.repetition_check=repetition_checker()

        self.service =None
        self.servers={}

        self.servers_and_methods=self.get_action()


    def get_service(self):
        
        '''
            This fetches the service that will be sent an attack
            count number of services in db
            generate a random service id for service to target
        '''
        try:
            service_count=self.data.service_count
            print('---------Gott service--------')

            service=random.randint(1,service_count)

            service_id=None

            if service ==1:#>1 and service<250:#SSH Server
                service_id= self.data.get_service(1)
            elif service ==2:#>250 and service<500:#FTP Server
                service_id = self.data.get_service(2)
            elif service ==3:#>500 and service<=750:#Web Server
               service_id = self.data.get_service(1)

            checker=rep.check(service_id['service_id'])

            if checker==False:#checking if the service was just selected

                rep.old_val=service_id['service_id']

                self.service=service_id

                servers=self.data.get_servers(service_id['service_id'])
                self.servers=servers


                return service_id
            else:
                print('service exists, getting another')
                self.get_service()

        except Exception as e:
            print (str(e))
            log.exception(e)

    def get_action(self):
        '''
        get a list of possible actions for that service
        get random id based how many items service
        check size of random action id against length of action list
        if size is the same we -1 from the id to avoid index range exception
        '''
        try:
            self.get_service()
            service_id=self.service['service_id']

            action_list=self.data.get_action(service_id)

            servers_and_methods=[]

            server_count=len(self.servers)

            def get_method():
                action_count=len(action_list)
                if action_count>1:
                    action_count=action_count-1
                    index=random.randint(0,action_count)
                else:index=0
                return action_list[index]['method']

            for i in range(0,server_count):
                servers_and_methods.append({'server':self.servers[i],'method':get_method()})


        except Exception as e:
            print (str(e))
            log.exception(e)
        self.servers_and_methods=servers_and_methods

        return servers_and_methods

    def get_ftp_user(self):
        users=self.data.get_ftp_users()
        count=len(users)-1
        i=random.randint(0,count)

        return users[i]
