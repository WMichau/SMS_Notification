import imaplib
import email
from dotenv import load_dotenv
import os
import re
import schedule
import time
from datetime import date
import sys
import datetime
from twilio.rest import Client
    
account_sid = ''
auth_token = ''

client = Client(account_sid, auth_token)

def readMails():

    counter = 0

    load_dotenv()
    username = os.environ.get('USERNAME')
    app_password= os.environ.get('PASSWORD')

    gmail_host= 'imap.gmail.com'
    mail = imaplib.IMAP4_SSL(gmail_host)
    mail.login(username, app_password)

    mail.select("MilleSMS")

    _, selected_mails = mail.search(None, '(FROM "chester12123@gmail.com")')

    #print("Total Messages from noreply@kaggle.com:" , len(selected_mails[0].split()))

    for num in selected_mails[0].split():
        _, data = mail.fetch(num , '(RFC822)')
        _, bytes_data = data[0]

        #convert the byte data to message

        email_message = email.message_from_bytes(bytes_data)
        #access fulldata
        #python main.py | grep Kwota | tr -d '-' | sed 's/,/\./' | awk '{ SUM += $2} END { print SUM }'
        
        #print("Subject: ",email_message["subject"])
        #print("To:", email_message["to"])
        #print("From: ",email_message["from"])
        #print("Date: ",email_message["date"])

        for part in email_message.walk():
            if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                message = part.get_payload(decode=True)
                
                sf = open('temp.txt', 'w')
                print(message.decode(), file = sf)
                sf.close()

                with open ('temp.txt', 'r') as f:
                    for line in f:
                        if 'Kwota' in line:
                            line = line.strip().replace('-', '').replace(',', '.')
                            result = re.findall("[+-]?\d+\.\d+", line)
                            for el in range (0, len(result)):
                                counter = counter + float(result[el])
                break
    
def SendSMS():

    message = client.messages \
        .create(
            body="HI",
            from_ = +19898001204,
            to = +48515941721
        )
    print(message.sid)
    #current_counter = 0
    #readMails()
    #if current_counter != counter:
        #SENDSMS
        #current_counter = counter


SendSMS()
######################################
#schedule.every(30).day.do(counter = 0)
#schedule.every(30).minutes.do(SendSMS)
######################################

#While True:
#     schedule.run_pending()
#     time.sleep(1)