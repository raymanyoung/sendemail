# -*- coding: utf-8 -*-
import re
import codecs

file = codecs.open('email.txt', 'r', encoding='utf-8')
# Create a text/plain message
content = file.read()

pattern = u"\w+[.|\w]\w+@\w+[\.]\w+[.|\w+]\w+"
prog = re.compile(pattern)

result = prog.findall(content)

print(result)