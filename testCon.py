import pymysql
import re
import random

class employees():
    def __init__(self):
        self.mysql_connection2 = self.get_mysql_connection2()
        self.employee_list = None

    def get_mysql_connection2(db_file): #mysql db connection
        '''
        Opens a new connection to the database, and returns the connection object to the caller.
        '''
        connection2 = None
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
            for i in range(0,10):
                print("exes")
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

Test1 = employees()
the_list = Test1.select_employees()
