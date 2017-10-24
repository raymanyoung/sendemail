# Import smtplib for the actual sending function
import smtplib
import codecs
import time

# Import the email modules we'll need
from email.mime.text import MIMEText

textfile = 'content.txt'
subjectfile = 'subject.txt'
emailfile = 'lists/list.txt'
accountfile = 'accounts/account.txt'
interval = 20 
smtp = ''
port = 0


# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
file = codecs.open(textfile, 'r', encoding='utf-8')
# Create a text/plain message
c = file.read()
file.close()

sf = codecs.open(subjectfile, 'r', encoding = 'utf-8')
subject = sf.read()
sf.close()

f = codecs.open(accountfile, 'r', encoding = 'utf-8')
me = f.readline().strip()
password = f.readline().strip()
smtp = f.readline().strip()
port = int(f.readline().strip())
sender = f.readline().strip()
	
print(me, password, smtp, port)

with open(emailfile, 'rb') as f:
    emails = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
emails = [x.strip() for x in emails] 

#msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
#       % (me, to, subject))

#msg = msg + c
#print('msg: ' + msg)


username= me

i = 0

with open('sent', 'a') as sentRecord:
	with open('invalid', 'a') as invalidRecord:

		for add in emails :
			if i ==  0 :
				print("establishing new connection...")
				s = smtplib.SMTP(smtp, port)

				s.starttls()
				print("connection established, logging in")
				s.login(username, password)

			i = i + 1
			if i > 10 :
				i = 0

			msg = MIMEText(c, "plain", 'utf-8')
			msg['Subject'] = subject
			msg['From'] = sender + ' <' + me + '>'
			msg['To'] = add
			
			# Send the message via our own SMTP server, but don't include the
			# envelope header.
			print('sending email to ' + add)
			try:
				s.sendmail(me, [add], msg.as_string())
				print('sent. Waiting...')
				sentRecord.write(add)
			except smtplib.SMTPRecipientsRefused as e:
				print("invalid address " + add)
				print(e.recipients)
				invalidRecord.write(add)

			time.sleep(interval)
		s.quit()
	
