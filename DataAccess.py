from cgi import valid_boundary

import pymysql
import re
import random
import logging as log

log.basicConfig(filename='dataAccess.log',level=log.DEBUG)


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
        result=None
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
            sql+="WHERE username LIKE 'ftpuser%' "
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
            sql+="WHERE username LIKE 'ftp' OR username LIKE 'a%' "
            connection = self.mysql_connection

            with connection as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                self.ftp_anon_user_result=result

        except Exception as e:
            print(str(e))
            log.exception(e)
        return self.ftp_anon_user_result

    def record_transaction(self,service_id,server_id,action_id):
        result=None
        try:
            sql='INSERT INTO transactions(service_id,server_id,action_id,date_time,test_date) '
            sql+="VALUES (%s,%s,%s,NOW(),NOW()) "

            connection = self.mysql_connection

            with connection as cursor:
                cursor.execute(sql,(service_id,server_id,action_id))

                connection.commit()

                # result = cursor.lastrowid()
                #
                # if result>0:
                #     return True
                # else:return False

        except Exception as e:
            print(str(e))
            log.exception(e)


class repetition_checker():
    def __init__(self):
        #print("repetition class initiated")
        self.history=[]
        self.checks=0

    def add(self,val):
        self.checks=self.checks+ val

    def check(self,value):
        #print("checking in service")
        #print('check no',self.checks)
        #print(self.history)

        if value in self.history: #if service selected is
            #print('serivce used ')
            #print(self.history)
            #print('true')

            return True

        elif value not in self.history:
            self.history.append(value)
            #print('getting data for ', value)
            #print('false')
            self.add(1)
            return False
        #print('returning nothing')

rep=repetition_checker()

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
        self.get_service()  #run method that will select the service to attack
        service_id=self.service['service_id'] #get the id of the select to attack

        #print('service',service_id)

        action_list=self.data.get_action(service_id)#gets a list of actions/attacks based on service selected
        action_count=len(action_list)#counts the number of actyions/attacks in the list

        servers_and_methods=[]#list that will store the server and its methods
        methods=[]#list that will store the methods of a service

        server_count=len(self.servers)#count the number of servers for a specific service e.g number of services for ssh service

        random_actions=[]

        #print('server count',server_count)
        #print('method count', action_count)
        try:
            if server_count == 1:#if there is only one server a service
                #print('if')
                while len(methods)<action_count:
                     #print('while')
                     random_action=random.randint(0,action_count-1)

                     if random_action in random_actions:
                          #print('small if')
                          pass
                     else:
                          random_actions.append(random_action)
                          methods.append(action_list[random_action])

                servers_and_methods.append({'server':self.servers[0],'method':methods})#store server and methods as index in servers_and_methods list


            else:
                #print('else')
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
        except Exception as e:
            print(e)
            log.exception(e)

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

    def record_transcation(self,server_id,service_id,action_id):

        try:
            self.data.record_transcation(service_id,server_id ,action_id)
        except Exception as e:
            print(e)
            log.exception(e)
''''
class attackList():
    def __init__(self):
        self.attList=[]
    def append_list(self,list):
        self.attList.extend(list)

    def get_list(self):
        l=[]
        list_size=len(self.attList)
        random_indexes=[]

        while len(random_indexes)<list_size:
            random_index=random.randint(0,list_size-1)
            if random_index in random_indexes:
                pass
            else:
                l.append(self.attList[random_index])
                random_indexes.append(random_index)
        return  l
'''
class builder():
    def __init__(self):
        #self.attList=attackList()# instantiate class attackList class
        self.attDic={}
        self.data=DataAccess()# instantiate class data access class
        #self.attacker=attacker()

    def build(self):
        #attackerObj=attacker()
        service_count=self.data.service_count

        #print('service count', service_count)
        dic_index=0
        for i in range(0,service_count):
            attackerObj=attacker()

            list=attackerObj.servers_and_methods

            #print('==========list')
            #print('service',attackerObj.service )
            #print(list)
            try:
                my_dic = {}

                count = len(attackerObj.servers_and_methods)
                service = attackerObj.service
                servers = attackerObj.servers_and_methods

                serversList=servers[0]
                action_count=len(serversList['method'])

                if count == 1:
                    for i in range(0,action_count):
                        item = [{'Service': service['service_name'],'service_id':service['service_id'],'server_id':servers[0]['server']['server_id'] ,'IP': servers[0]['server']['ip_addr'],
                        'User': servers[0]['server']['username'], 'Password': servers[0]['server']['password'],'method_id':servers[0]['method'][i]['action_id'],
                        'Method': servers[0]['method'][i]['method']}]

                        #my_dic[i] = item
                        self.attDic[dic_index]=item
                        dic_index=dic_index+1



                else:
                    #print('else')
                    item_list=[]
                    for i in range(0, count):
                        #print('main for')
                        #print(servers[i]['server']['ip_addr'])

                        for j in range(0,action_count-1):
                            #print('child for')
                            item = [{'Service': service['service_name'],'service_id':service['service_id'],'server_id':servers[i]['server']['server_id'] ,'IP': servers[i]['server']['ip_addr'],
                            'User': servers[i]['server']['username'], 'Password': servers[i]['server']['password'],'method_id':servers[i]['method'][j]['action_id'],
                            'Method': servers[i]['method'][j]['method']}]

                            item_list.append(item)

                    for i in range(0,len(item_list)):
                        #my_dic[i]=item_list[i]
                        self.attDic[dic_index]=item_list[i]
                        dic_index=dic_index+1

                #self.attList.append_list(my_dic)


            except Exception as e:
                print (str(e))
                log.exception(e)

        # my_dic=self.attDic
        # for i in range(0,len(my_dic)):
        #     print(i)
        #     print(my_dic[i])
        #     print('\n')

    def get_list(self):
        list={}
        list_size=len(self.attDic)
        #print('list size',list_size)
        random_indexes=[]

        count=0
        while len(random_indexes)<list_size:
            random_index=random.randint(0,list_size-1)
            if random_index in random_indexes:
                pass
            else:
                list[count]=self.attDic[random_index]
                random_indexes.append(random_index)
                count=count+1


        #print(self.attDic)

        #print(len(list))
        #
        # for i in range(0,len(list)):
        #     print(i)
        #     print(list[i])
        #     print('\n')
        return list

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
            sql='SELECT * FROM employees e, salaries s, dept_emp d where s.emp_no = e.emp_no LIMIT 100'
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


# b=builder()
# b.build()
# b.get_list()
#print('\n')

# list=b.attList.attList
# for key,val in list:
#     print(val)
#     print('\n')

# attList=attackList()
# l=attList.get_list()
# print('size of l',len(l))
# for i in range(0,len(l)):
#     print(l[i])

#att=attacker()
#
# list=att.servers_and_methods
# print(list)


