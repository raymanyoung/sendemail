import poplib
import codecs
from email import parser
import re

def displaymatch(match):
    if match is None:
        return "None"
    return '<Match: %r, groups=%r>' % (match.group(), match.groups())

accountfile = 'accounts/account.txt'

f = codecs.open(accountfile, 'r', encoding = 'utf-8')
username = f.readline().strip()
password = f.readline().strip()
stmp = f.readline().strip()
port = int(f.readline().strip())
pop = f.readline().strip()
popport = int(f.readline().strip())
sender = f.readline().strip()
f.close()

pop_conn = poplib.POP3_SSL(pop, popport)
pop_conn.user(username)
pop_conn.pass_(password)
#Get messages from server:
count = len(pop_conn.list()[1]) + 1
messages = [pop_conn.retr(i) for i in range(count - 1, count)]
# Concat message pieces:
messages = ["\n".join(mssg[1]) for mssg in messages]
#Parse message intom an email object:
messages = [parser.Parser().parsestr(mssg) for mssg in messages]

pattern = r"\w+[.|\w]\w+@\w+[\.]\w+[.|\w+]\w+"
prog = re.compile(pattern)

for message in messages:
    s = str(message) 
    result = prog.findall(s)
    print(result[3])
pop_conn.quit()