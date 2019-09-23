import json
import smtplib, ssl
import os
from email.message import EmailMessage
import db_functions 
from datetime import datetime

## Helper functions Start


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }
## Helper functions End

#Function for Raising Request
def RaiseRequest(intent_request):
  userEmail=intent_request['currentIntent']['slots']['userEmail']
  ticketSubject=intent_request['currentIntent']['slots']['ticketSub']
  ticketBody=intent_request['currentIntent']['slots']['ticketBody']

  session_attributes = intent_request['sessionAttributes'] 
  mainusername=session_attributes['mainuser']
  if intent_request['invocationSource']=='DialogCodeHook':
    validation_result = Slot_Validation(intent_request['currentIntent']['slots'])
    if not validation_result['isValid']:
            slots = intent_request['currentIntent']['slots']
            slots[validation_result['violatedSlot']] = None

            return elicit_slot(
                session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                validation_result['message']
            )
    return delegate(session_attributes, intent_request['currentIntent']['slots'])
  try:
    s=sendEmail(userEmail,mainusername,ticketSubject,ticketBody)
  except:
      return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Error Raised'
        }
    )
  return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Ticket #{}, has been raised and will be resolved soon. Please check your mail for further info.'.format(s[1])
        }
    )
  
def AutoWelcomeMessage(intent_request):
  user_name=intent_request['currentIntent']['slots']['userName']
  session_attributes = intent_request['sessionAttributes']
  session_attributes['mainuser']=user_name
  return delegate(session_attributes, intent_request['currentIntent']['slots'])


def Slot_Validation(slot):
  user_Email=slot['userEmail']
  if(user_Email == os.environ['SENDER_EMAIL']):
      return build_validation_result(
            False,
            'userEmail',
            'This email ID {} is not valid. Please provide valid email ID'.format(user_Email)
        )
  return {'isValid': True}
  
def build_validation_result(isvalid, violated_slot, message_content):
    return {
        'isValid': isvalid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
}

#Send Email Function
def sendEmail(r_email,r_username,ticketSubject,ticketBody):
  msg=EmailMessage()
  host=os.environ['SMTPHOST']
  port=os.environ['SMTPPORT']
  sender_email=os.environ['SENDER_EMAIL']
  sender_password=os.environ['SENDER_PASSWORD']
  #generaating unique id
  id_tuple=db_functions.query_record('select max(id) from requests_tab',1)
  if(id_tuple[0]==None):
    id=0
  else:
    id=id_tuple[0]
  id=id+1
  context=ssl.create_default_context()
  message_to_user="""
  Hi """+r_username+""",
  
  Thanks for writing to us. We have received your Query. One of our representative will reply to you shortly.
  
  Your Query: """+ticketBody+"""

  Thanks,
  Kraftcache Team
  
  Note: This mail is an acknowledgment for your ticket raised with our Chatbot"""
  
  msg.set_content(message_to_user)
  msg['Subject']='Ticket #'+str(id)+' - ' + ticketSubject
  msg['From']=sender_email
  msg['To']=r_email
  msg['Bcc']=os.environ['BCC']
  msg['Reply-To']=r_email
  #sending mail
  with smtplib.SMTP_SSL(host,port,context=context) as server:
    try:
      server.login(sender_email,sender_password)
      db_functions.insert_records(id,r_username,r_email,ticketSubject,ticketBody,'OPEN',datetime.now())
      server.send_message(msg)
      server.close()
      status=['True',id]
    except:
      status=['False',id]
  return status


def lambda_handler(event, context):
  intent= event['currentIntent']['name']
  if intent=='RaiseRequest':
      return RaiseRequest(event)
  if intent=='AutoWelcomeMessage':
      return AutoWelcomeMessage(event)