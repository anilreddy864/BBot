# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 15:07:13 2019

@author: anilreddy.tirugudu
"""

import smtplib, ssl
from email.message import EmailMessage



def sendEmail(r_email,r_username,ticketSubject,ticketBody):
  msg=EmailMessage()
  port=465
  sender_email='admin@kraftcache.com's
  sender_password='Anil@3669'
  context=ssl.create_default_context()
#Message to User
  message_to_user="""
  Hi """+r_username+""",
  
  Thanks for writing to us. We have received your Query. One of our representative will reply you shortly.
  
  Your Query: """+ticketBody+"""

  Thanks,
  Kraftcache Team
  Note: This mail is an acknowledgment for your ticket raised with our Chatbot"""
  
  msg.set_content(message_to_user)
  msg['Subject']='Ticket Raised - ' + ticketSubject
  msg['From']=sender_email
  msg['To']=[r_email,'anilreddyt.1234@gmail.com']
  #msg['Bcc']='anilreddyt.1234@gmail.com'
#

  with smtplib.SMTP_SSL('sg3plcpnl0193.prod.sin3.secureserver.net',port) as server:
    try:
      server.login(sender_email,sender_password)
      server.send_message(msg)
      status='True'
    except Exception as e:
      raise e
  return status

print(sendEmail('anilreddy864@gmail.com','Anil','Sub','Body'))