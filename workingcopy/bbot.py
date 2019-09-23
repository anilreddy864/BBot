# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 13:43:27 2019

@author: anilreddy.tirugudu
"""
import smtplib, ssl
from email.message import EmailMessage

msg=EmailMessage()
port=465
email='anilreddyt.1234@gmail.com' #input('Enter Email:')
password='Anil@3669' #input('Enter Password:')
d_email='anilreddy864@gmail.com' #input('Enter Output Email:')
context=ssl.create_default_context()
message="We have received your request. Your Issue will be resolved soon"

msg.set_content(message)
msg['Subject']='Ticket Raised - Delivery not received yet'
msg['From']=email
msg['To']=d_email


with smtplib.SMTP_SSL('smtp.gmail.com',port,context=context) as server:
    server.login(email,password)
    server.send_message(msg)
    #server.sendmail(email,t_email,message)
    print('mail sent')