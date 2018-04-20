import pymysql
import re
import random
import logging as log

log.basicConfig(filename='dataAccess.log',level=log.DEBUG)

class repetition_checker():
    def __init__(self):
        #print("repetition class initiated")
        self.old_val=0

    def check(self,value):
        #print("check")
        #print(value)
        if self.old_val==value:
            self.old_val=value
            return True
        return False

rep=repetition_checker()


class DataAccess():
    def __init__(self):
        self.mysql_connection = self.get_mysql_connection()
        self.service_count=self.count_services()
        self.ftp_user_result=None
        self.ftp_anon_user_result=None

    def get_mysql_connection(db_file): #mysql db connection
        '''
        Opens a new connection to the database, and returns the connection object to the caller.
        '''
        connection = None
        try:
            # get database configuration from database.txt
            text_file = open("database.txt", "r")
            #lines = re.split(',', text_file.read())
            lines=text_file.read().split(',')
            hostname = lines[0]
            username = lines[1]
            password = lines[2]
            database = lines[3]#'127.0.0.1'
            #print(database)
            connection = pymysql.connect(host=hostname, user=username, password=password, database=database, cursorclass=pymysql.cursors.DictCursor)

            #connection = pymysql.connect(host='10.0.5.43', user='myuser', password='1234', database='ir_db',cursorclass=pymysql.cursors.DictCursor)
            #connection = pymysql.connect(host='192.168.8.126', user='myuser', password='1234', database='ir_db',cursorclass=pymysql.cursors.DictCursor)#host=146.64.182.136
            #print('connected')
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
            #result=self.query_exec(sql)
            connection = self.mysql_connection

            with connection as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()

        except Exception as e:
            print(str(e))
            log.exception(e)
            
        return result

    def count_services(self):
        sql='SELECT COUNT(service_id) as count FROM service'
        connection = self.mysql_connection

        with connection as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
        return result['count']

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
        result=None
        try:
            sql='SELECT user_id,username,password '
            sql+="FROM ftp_users "
            sql+="WHERE username LIKE 't%' "
            #result=self.query_exec(sql)
            connection = self.mysql_connection

            with connection as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                self.ftp_user_result=result

        except Exception as e:
            print(str(e))
            log.exception(e)
        return self.ftp_user_result

    def get_ftp_anon_users(self):
        result=None
        try:
            sql='SELECT user_id,username,password '
            sql+="FROM ftp_users "
            sql+="WHERE username LIKE 'f%' OR username LIKE 'a%' "
            connection = self.mysql_connection

            with connection as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                self.ftp_anon_user_result=result

        except Exception as e:
            print(str(e))
            log.exception(e)
        return self.ftp_anon_user_result

    def record_transcation(self,service_id,server_id,action_id,test_id):
        result=None
        try:
            sql='INSERT INTO transactions(service_id,server_id,action_id,date_time,test_id) '
            sql+="VALUES (%s,%s,%s,NOW(),%s) "

            connection = self.mysql_connection

            with connection as cursor:
                cursor.execute(sql,(service_id,server_id,action_id,test_id))

                connection.commit()

                # result = cursor.lastrowid()
                #
                # if result>0:
                #     return True
                # else:return False

        except Exception as e:
            print(str(e))
            log.exception(e)


class attacker(object):
    def __init__(self):
        #print("attacker class initiated")
        self.data=DataAccess()
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
            #print('---------Gott service--------')

            service=random.randint(1,service_count)

            service_id=None

            if service ==1:#>1 and service<250:#SSH Server
                service_id= self.data.get_service(1)
            elif service ==2:#>250 and service<500:#FTP Server
                service_id = self.data.get_service(2)
            elif service ==3:#>500 and service<=750:#Web Server
               service_id = self.data.get_service(3)
            elif service ==4:#>500 and service<=750:#Web Server
               service_id = self.data.get_service(4)

            checker=rep.check(service_id['service_id'])

            if checker==False:#checking if the service was just selected

                rep.old_val=service_id['service_id']

                self.service=service_id

                servers=self.data.get_servers(service_id['service_id'])
                self.servers=servers

                return service_id
            else:
                #print('service exists, getting another')
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
        self.get_service()  #run method that will select the service to attack
        service_id=self.service['service_id'] #get the id of the select to attack

        action_list=self.data.get_action(service_id)#gets a list of actions/attacks based on service selected
        action_count=len(action_list)#counts the number of actyions/attacks in the list

        servers_and_methods=[]#list that will store the server and its methods
        methods=[]#list that will store the methods of a service

        server_count=len(self.servers)#count the number of servers for a specific service e.g number of services for ssh service

        random_actions=[]

        if server_count == 1:#if there is only one server a service

            while len(methods)<=action_count:
                 random_action=random.randint(0,action_count-1)

                 if random_action in random_actions:
                      pass
                 else:
                      random_actions.append(random_action)
                      methods.append(action_list[random_action])

            servers_and_methods.append({'server':self.servers[0],'method':methods})#store server and methods as index in servers_and_methods list


        else:
            for i in range(0,server_count):
                while len(methods)<action_count:
                    random_action=random.randint(0,action_count-1)

                    if random_action in random_actions:
                        pass
                    else:
                        random_actions.append(random_action)
                        methods.append(action_list[random_action])

                servers_and_methods.append({'server':self.servers[i],'method':methods})

                methods=[]
                random_actions=[]


        self.servers_and_methods=servers_and_methods

        return servers_and_methods

    def get_ftp_user(self):
        users=self.data.get_ftp_users()
        count=len(users)-1
        i=random.randint(0,count)

        return users[i]

    def get_ftp_anon_user(self):
        users=self.data.get_ftp_anon_users()
        count=len(users)-1
        i=random.randint(0,count)

        return users[i]

    def record_transcation(self,test_id):
        list = self.servers_and_methods
        list_size=len(list)
        service = self.service

        try:
            for i in range(0, list_size):
                service_id = service['service_id']
                server_id = list[i]['server']['server_id']
                action_id = list[i]['method']['action_id']
                the_id = str(test_id)
                insert=self.data.record_transcation(service_id,server_id ,action_id,the_id)

                if i == (list_size - 1):
                    break

        except Exception as e:
            print(e)
            log.exception(e)
            print()
class employees(object):
    def __init__(self):
        self.mysql_connection2 = self.get_mysql_connection2()
        self.employee_list = None

    def get_mysql_connection2(self): #mysql db connection
        '''
        Opens a new connection to the database, and returns the connection object to the caller.
        connection2 = None
        '''
        try:
            # get database configuration from database.txt
            text_file = open("database2.txt", "r")
            lines = re.split(',', text_file.read())
            #lines=text_file.read().split(',')
            hostname = lines[0]
            username = lines[1]
            password = lines[2]
            database = lines[3]

            connection2 = pymysql.connect(host=hostname, user=username, password=password, database=database, cursorclass=pymysql.cursors.DictCursor)

        except Exception as e:
            print("Error: Could not connect to the database.\n")
            print("Checka di Settings.\n")
            print(str(e))
            exit()

        return connection2

    def select_employees(self):
        result=None
        try:
            sql='SELECT * FROM employees e, salaries s, dept_emp d where s.emp_no = e.emp_no'
            connection = self.mysql_connection2

            with connection as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                self.employee_list=result

        except Exception as e:
            print(str(e))
        return self.employee_list

    def drop_table(self):
        result=None
        try:
            sql="DROP DATABASE employees"

            connection = self.mysql_connection2

            with connection as cursor:
                cursor.execute(sql)

                connection.commit()

        except Exception as e:
            print(str(e))

att=attacker()

#list=att.get_action()
#print(list)
