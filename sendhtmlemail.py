# Import smtplib for the actual sending function
import smtplib
import codecs
import time
import math


# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


textfile = 'html2.html'
subjectfile = 'subject.txt'
emailfile = 'lists/list.txt'
accountfile = 'accounts/account.txt'
interval = 60 #interval in seconds between 2 sendings
smtp = ''
port = 0
emailNumberToReconnect = 7   # number of emails sent before next reconnect to server (the connection could timeout)


# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
file = codecs.open(textfile, 'r', encoding='utf-8')
# Create a text/plain message
content = file.read()
file.close()

sf = codecs.open(subjectfile, 'r', encoding = 'utf-8')
subject = sf.read()
sf.close()

f = codecs.open(accountfile, 'r', encoding = 'utf-8')
me = f.readline().strip()
password = f.readline().strip()
smtp = f.readline().strip()
port = int(f.readline().strip())
pop = f.readline().strip()
popport = int(f.readline().strip())
sender = f.readline().strip()
f.close()

print(me, password, smtp, port)

with open(emailfile, 'rb') as f:
    emails = f.readlines()
emails = [x.strip() for x in emails] 

i = 0
batch = 10


def login(smtp, port, username, password):
    print("establishing new connection...")
    s = smtplib.SMTP(smtp, port)

    s.starttls()
    print("connection established, logging in")
    s.login(username, password)    
    return s
    
def sendMail(targets, conn):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender + ' <' + me + '>'
    msg['To'] = ",".join(target)
    
    msg.attach(part1)
    
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    print('sending email to ' + msg['To'])
    try:
        conn.sendmail(me, target, msg.as_string())
        print('sent. Waiting...i')
        sentRecord.write(msg['To'] + "\r\n")
    except smtplib.SMTPRecipientsRefused as e:
        print("invalid address " + msg['To'] )
        print(e.recipients)
        invalidRecord.write(msg['To'] + "\r\n")
    except smtplib.SMTPDataError as e:
        print(e)
        print("SMTPDataError: " + msg['To'])               
        invalidRecord.write(msg['To'])
    except smtplib.SMTPServerDisconnected:
        print("establishing new connection...")
        conn = login(smtp, port, me, password)
        conn.sendmail(me, targets, msg.as_string())
        print('sent. Waiting...i')
        sentRecord.write(msg['To'] + "\r\n")

with open('sent', 'a') as sentRecord:
    with open('invalid', 'a') as invalidRecord:

        part1 = MIMEText(content, "html", 'utf-8')    
    
        allcount = len(emails)
        print("address count: ", allcount)
        target = []
        for index in range (0,  allcount):
            if index % batch == 0:
                count = batch
                if count > allcount - index:
                    count = allcount - index
                target = range(0, count)
                
            target[index % batch] = emails[index]
            if index % batch == batch - 1 or index == allcount - 1:
        
                if i ==  0 :
                    s = login(smtp, port, me, password)

                i = i + 1
                if i > emailNumberToReconnect :
                    i = 0
                print(target)
                sendMail(target, s)

                time.sleep(interval)

