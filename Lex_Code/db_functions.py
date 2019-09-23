import pymysql
import os
from datetime import datetime

   
def query_record(query,count):
    connection=set_con()
    cursor = connection.cursor()
    if(connection.open):
        cursor.execute(query)
        if(count==1):
            records=cursor.fetchone()
        else:
            records=cursor.fetchAll()
        return records        
        
def insert_records(id,name,email,tSub,tBody,status,date):
    connection=set_con()
    cursor = connection.cursor()
    try:
        if(connection.open):
            query="""INSERT INTO requests_tab (id,name,email,ticket_sub,ticket_body,status,date) 
                     VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            parameters=(id,name,email,tSub,tBody,status,date)
            cursor.execute(query,parameters)
            connection.commit()
            return 'True'
    except:
        return 'False'

# Open database connection
def set_con():
    connection = pymysql.connect(host=os.environ['DB_HOST'],
                                         port=int(os.environ['DB_PORT']),
                                         user=os.environ['DB_USERNAME'],
                                         password=os.environ['DB_PASSWORD'],
                                         database=os.environ['DB_NAME'])
    return connection

        