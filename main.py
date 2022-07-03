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
    
load_dotenv()
username = os.environ.get('USERNAME')
app_password= os.environ.get('PASSWORD')
account_sid = os.environ.get('SID')
auth_token = os.environ.get('TOKEN')

client = Client(account_sid, auth_token)

current_counter = 0

def deleteMails():  
    
    gmail_host= 'imap.gmail.com'
    mail = imaplib.IMAP4_SSL(gmail_host)
    mail.login(username, app_password)

    mail.select("MilleSMS")

    status, messages = mail.search(None, 'FROM "chester12123@gmail.com"')

    messages = messages[0].split(b' ')
    
    if messages[0] != b'':
        for maill in messages:
            _, msg = mail.fetch(maill, "(RFC822)")
            mail.store(maill, "+FLAGS", "\\Deleted")
        mail.expunge()
        mail.close()
        mail.logout()

def readMails():

    counter = 0
    f = open("temp.txt", "a")

    gmail_host= 'imap.gmail.com'
    mail = imaplib.IMAP4_SSL(gmail_host)
    mail.login(username, app_password)

    mail.select("MilleSMS")

    _, selected_mails = mail.search(None, '(FROM "chester12123@gmail.com")')

    for num in selected_mails[0].split():
        _, data = mail.fetch(num , '(RFC822)')
        _, bytes_data = data[0]

        email_message = email.message_from_bytes(bytes_data)
        #python main.py | grep Kwota | tr -d '-' | sed 's/,/\./' | awk '{ SUM += $2} END { print SUM }'

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

    return counter

def SendSMS():

    global current_counter

    readMails()
    counter = readMails()

    if current_counter != counter:
        current_counter = counter
        message = client.messages \
          .create(
              body="Wydane: " + str(current_counter) + " PLN",
              from_ = +19898001204,
              to = +48515941721
            )
    #print(counter)
    #print(current_counter)
    os.remove("temp.txt")
 
#deleteMails()
#readMails()
#SendSMS()
############################################
schedule.every(30).days.do(deleteMails)
schedule.every(5).seconds.do(SendSMS)
############################################

while True:
     schedule.run_pending()
     time.sleep(1)