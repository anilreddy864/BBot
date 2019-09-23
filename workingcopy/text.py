import pymysql
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
            parameters=(name,email,tSub,tBody,status,date)
            cursor.execute(query,parameters)
            connection.commit()
            return 'True'
    except:
        return 'False'
    
def set_con():
    connection = pymysql.connect(host='148.66.145.18',
                                     port=3306,
                                     user='anilreddy',
                                     password='anilreddy',
                                     database='kraftcache_requests_db')
    
    return connection
