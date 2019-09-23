import pymysql
from datetime import datetime

def select_records(id):
    if(connection.open):
        query="""select * from requests_tab where id=%s"""
        cursor.execute(query,(id,))
        print(query)
        records=cursor.fetchone()
        return records
        
    print(records[6].strftime("%d/%m/%Y %H:%M:%S"))
# Open database connection

def insert_records(name,email,tSub,tBody,status,date):
    try:
        if(connection.open):
            query="""INSERT INTO requests_tab (name,email,ticket_sub,ticket_body,status,date) 
                     VALUES (%s,%s,%s,%s,%s,%s)"""
            parameters=(name,email,tSub,tBody,status,date)
            cursor.execute(query,parameters)
            connection.commit()
            return 'True'
    except:
        return 'False'

connection = pymysql.connect(host='148.66.145.18',
                                     port=3306,
                                     user='anilreddy',
                                     password='anilreddy',
                                     database='kraftcache_requests_db')
if(connection.open):
    db_Info = connection.get_server_info()
    cursor = connection.cursor()
    cursor.execute("select database();")
    record = cursor.fetchone()
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")	
    #status_insert=insert_records('Aravind','123@gmail.com','tSub','tBody','OPEN',datetime.now())
    select_records(6)
cursor.close()


        