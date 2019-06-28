emailto=['abc@abc.com']      # Provide an email where want to send CSV file.
emailfrom='xyz@xyz.com'        # Provide a valide from email.
password='*******'	         # Provide the correct password for your from mail.
smtpserver='ZZZZZZ'             # Provide a valid server ,for example: smtp.gmail.com
port=587                        #Provide a valid port number

sendmail=1 ## [1 sends mail or 0 does not send mail] if sendmail=1 then user have to set the required information to send out a email from the code.
msgbody=r'''Hi

Please find the attachment for the Endpoints SPMLogs in Text file format.

Thank you.'''

si=[]
e=[]
b=[]
d="Rmm_dll"
import os
import re
import random
import socket
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

fileToSend=os.path.join(os.environ['TEMP'], 'report.txt')

def computername():
    return os.environ['COMPUTERNAME']

def ipaddress():
    return socket.gethostbyname(socket.gethostname())

def emailreport(subject, emailto,emailfrom,fileToSend,password,smtpserver,port,msgbody):
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = ",".join(emailto)
    msg["Subject"] = subject
    msg.preamble = subject
    body = MIMEText(msgbody)
    msg.attach(body)       
    with open(fileToSend, 'rb') as fp:
        record = MIMEBase('text', 'octet-stream')
        record.set_payload(fp.read())
        encoders.encode_base64(record)
        record.add_header('Content-Disposition', 'attachment', filename=os.path.basename(fileToSend))
        msg.attach(record)
    try:
        server = smtplib.SMTP(smtpserver,port)
        server.ehlo()
        server.starttls()
        server.login(emailfrom, password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
        return " \nThe email report has been sent to "+msg["To"]
    except Exception as e:
        return e



def getrmm(a):
    os.chdir(a)
    c=os.popen("dir").read()
    find=re.findall('SpmAgent.*',c)
    for i in find:
        if not i:
            print "\n There is no SPMLogs folders are available in specified Endpoint"
        else:
            b.append(a+'\\'+i)
            
                
    for i in b:
        with open (i, 'r+') as file:
            for line in file:
                string=''
                line=line.strip()
                if 'Error' in line or 'Operation' in line or 'exit code' in line or 'Proxy configuration message' in line:
                    line=line+'\n'
                    if line=='':
                        continue
                    else:
                        line=line.strip()
                        si.append(line)
                        string+=''.join(line)
        with open(fileToSend,'w') as fr:
             if si:
                  for i in si:
                       fr.write('\n'+i)
             else:
                  fr.write("the Spm Agent is empty")
      
if 'PROGRAMFILES(X86)' in os.environ.keys():
    pmlpath=os.path.join(os.environ['PROGRAMFILES(X86)'], 'COMODO\\Comodo ITSM\\cpmlogs')
else:
    pmlpath=os.path.join(os.environ['PROGRAMFILES'], 'COMODO\\Comodo ITSM\\cpmlogs')
    

getrmm(pmlpath)
subject='%s %s CPM Logs report'%(computername(), ipaddress())


if sendmail==1:
    print emailreport(subject,emailto,emailfrom,fileToSend,password,smtpserver,port,msgbody)
    print 'mail send'
else:
    print " Set sendmail value as 1 "

