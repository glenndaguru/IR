#imports
import pymysql
import re
import random
#import bpy



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
        self.service_count=self.count_services()
        self.servers_per_service=self.count_server_service()
        self.steps=[]
        self.services=[]

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
            #connection = pymysql.connect(host='10.0.5.30', user='myuser', password='1234', database='ir_db',cursorclass=pymysql.cursors.DictCursor)
            connection = pymysql.connect(host='146.64.182.136', user='myuser', password='1234', database='ir_db',cursorclass=pymysql.cursors.DictCursor)
            print('connected')
        except Exception as e:
            print("Error: Could not connect to the database.\n")
            print("Checka di Settings.\n")
            print(str(e))
            exit()
        return connection

    def get_service(self,service_id):
        sql='SELECT s.service_id,s.service_name FROM service s '
        sql+="WHERE s.service_id="+str(service_id)
        sql+=" AND s.service_id != 3"
        #result=self.query_exec(sql)
        connection = self.mysql_connection

        with connection as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()

        return result

    def get_servers(self,service_id):
        sql='SELECT s.server_id,s.server_name,s.ip_addr,s.port,s.username,s.password '
        sql+="FROM servers s WHERE s.service="+str(service_id)
        #result=self.query_exec(sql)
        connection = self.mysql_connection

        with connection as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()

        return result

    def count_services(self):
        sql='SELECT COUNT(service_id) as count FROM service'
        connection = self.mysql_connection

        with connection as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
        return result['count']

    def count_server_service(self):
        sql='SELECT service , COUNT(server_id) FROM `servers` GROUP BY service'
        connection = self.mysql_connection

        with connection as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
        return result

    def get_action(self,service_id):
        sql='SELECT a.action_id, a.method FROM action a '
        sql+='INNER JOIN service s ON '
        sql +='s.service_id=a.service '
        sql+="WHERE a.service="+str(service_id)

        connection = self.mysql_connection

        with connection as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()

        return result

class attacker():
    def __init__(self):
        self.data=DataAccess()
        #self.temp_service_id=self.get_service()
        self.repetition_check=repetition_checker()

        self.service = None
        self.servers={}
        self.action=None
        self.actions=[]
        self.actions_list={}
        self.service_and_server_details={}
        self.attack_details={}


    def get_service(self):#This fetches the service that will be sent an attack
        service_count=2#self.data.count_services()#count number of services in db


        service=random.randint(1,service_count)#generate a random service id for service to target
        service_id=None


        if service ==1:#>1 and service<250:#SSH Server
            service_id= self.data.get_service(1)
        elif service ==2:#>250 and service<500:#FTP Server
            service_id = self.data.get_service(2)
        # elif service ==3:#>500 and service<=750:#Web Server
        #    service_id = self.data.get_service(3)

        checker=rep.check(service_id['service_id'])

        if checker==False:#checking if the service was just selected

            rep.old_val=service_id['service_id']

            self.service=service_id
            self.servers=self.data.get_servers(service_id['service_id'])

            self.attack_details['service']=self.service
            self.attack_details['servers']=self.servers

            return service_id
        else:
            self.get_service()

    def get_action(self):
        #service=self.get_service()
        print('-------we in get action----------')
        service=self.service

        service_id=service['service_id']
        action_list=self.data.get_action(service_id)#get a list of possible actions for that service
        #print(action_list)

        action_id=random.randint(1,len(action_list))#get random id based how many items service


        if action_id==len(action_list):#check size of random action id against length of action list
            action_id=action_id-1#if size is the same we -1 from the id to avoid index range exception


        action=action_list[action_id]


        self.action=action

        return action

    def fetch_action(self):
        self.get_service()#run this methood to get the service currently being used

        actions_list=[]

        server_count=len(self.servers)
        print('server_count')
        print(server_count)

        if server_count>1:#check if there is more than one server for a service
            service_id=self.service['service_id']
            # print('service_id')
            # print(service_id)
            for i in range(0,server_count,1):#genereate an action for each server

                self.get_action()#run this method to get an action
                action=self.action

                # print('-- ,?jk[-                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             -'/;/----------------------------------------------------------')
                # print(i)
                print ('get_action')
                print (action)

                if actions_list:#check if action list is empty
                    if action in actions_list:
                        print('---------------exists')
                        continue

                    else:
                        #print('-------------Adding items')
                        actions_list.append(action)

                else:actions_list.append(action)#if action list empty then just add action to action list
        else:#if there is only one service in db
            print('one service')
            self.actions=self.get_action()
        if actions_list:
            self.actions=actions_list

        self.attack_details['actions']=self.actions

        #
        # print('\n\n')
        # print('the list')
        # print(actions_list)




att=attacker()

# att.get_service()
# att.get_action()

att.fetch_action()

print(att.actions)
print(type(att.actions))
print(att.attack_details['actions'])
#print(att.service)

# server_count=2
# my_dic={}#lol
#
# for i in range(0,server_count,1):
#    data=attacker()
#    data.fetch_action()
#    #print(att.attack_details)
#    print ('-------------------------------------------')
#    service=data.attack_details['service']
#    servers=data.attack_details['servers']
#    actions=data.attack_details['actions']
#    # print(service)
#    # print(servers)
#    # print(action)    #get a random server to attacker
#    server_count=len(servers)-1
#    rand_server=random.randint(0,server_count)
#    server=servers[rand_server]
#
#    #print('Server')
#    #print(server)    #get a random method to execute on the server
#
#    action_count=len(actions)
#    action_id=random.randint(0,action_count)
#    action=actions[action_id-1]
#
#    #print ('action')
#    #print(action)
#    # items={'Service':service['service_name'],'IP':server['']['ip-addr'],'User':servers['']['username'],'Password':servers['']['password'],'Method':action['']['method'],}
#    items={'Service':service['service_name'],'IP':server['ip_addr'],'User':server['username'],'Password':server['password'],'Method':action['method']}
#    my_dic[i]=items
#
#    #  # deselect all
#    # bpy.ops.object.select_all(action='DESELECT')
#    #
#    #  # selection
#    # bpy.data.objects['attacker'].select = True
#
# # remove it
#
# print(len(my_dic))
# for i in range(0,len(my_dic),1):
#     print(i)
#     print(my_dic[i])
#     print('\n\n')
