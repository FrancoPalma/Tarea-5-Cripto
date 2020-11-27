import imaplib
import email
from email.header import decode_header
import os
import re
from getpass import getpass

username = "fpalmatrejo@gmail.com"
#password = ""
password = getpass("Ingrese las password: \n")
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(username, password)
imap.select("INBOX")

f = open("info.txt", "r")
leer = f.read().split()
de = leer[0]
desde = leer[1]
reg =leer[2]
typ, data  = imap.search(None,'FROM "'+de+'" SINCE "'+desde+'"')

l_msgid = []

for num in data[0].split():
    typ, data = imap.fetch(num, '(BODY[HEADER.FIELDS (MESSAGE-ID)])')
    msg_str = email.message_from_string(data[0][1].decode())
    message_id = msg_str.get('Message-ID')
    l_msgid.append(message_id)
count=1
for i in l_msgid:
    print("Correo n°: "+str(count)+".")
    print("Msg-Id: "+i)
    if(bool(re.match(reg, i))):
        print("Correo original.\n")
    else:
        print("Posible correo spoofing.\n")
    count+=1
print("="*25+"Se encontraron solo "+str(len(l_msgid))+" correos."+"="*25)
imap.close()
imap.logout()
