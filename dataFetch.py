''''
    the code below will select a single server and a single method.
    if there is more than one server, for each server a action/method/attack will be selected
'''     '''
        if server_count == 1:#if there is only one server a service 
            print('in if')
        
            print("action count ", action_count)
            for i in range(0,action_count): #get all the methods for that service and store in methods[]
                methods.append(action_list[i])
            servers_and_methods.append({'server':self.servers[0],'method':methods})#store server and methods as index in servers_and_methods list
            # for i in methods:
            #     print(i)
            print(servers_and_methods)
        else:
            print('in else')
            for i in range(0,server_count):
                for j in range(0,action_count):
                     methods.append(action_list[j])
                servers_and_methods.append({'server':self.servers[i],'method':methods})
        
            for i in servers_and_methods:
                print(i)
                print("\n")
        '''

        '''
        the code below will select a single server and a single method.
        if there is more than one server, for each server a action/method/attack will be selected
        '''
        # print("count ", server_count)
        #
        # def get_method():
        #     action_count=len(action_list)
        #     print("count ", action_count)
        #     if action_count>1:
        #         action_count=action_count-1
        #         index=random.randint(0,action_count)
        #     else:index=0
        #     return action_list[index]#['method']
        #
        # if server_count == 1:
        #     print('in if')
        #     servers_and_methods.append({'server':self.servers[0],'method':get_method()})
        # else:
        #     print('in else')
        #     for i in range(0,server_count):
        #         servers_and_methods.append({'server':self.servers[i],'method':get_method()})
        #
        #
        # self.servers_and_methods=servers_and_methods
