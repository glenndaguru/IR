import random

random_actions=[]

action_count=[1,2,3,4,5,6,7,8,9]
methods=[]

while len(methods)<=len(action_count):

    random_action=random.randint(0,len(action_count))


    if random_action in random_actions:
        pass
    else:
        random_actions.append(random_action)
        methods.append(random_action)

print(methods)

