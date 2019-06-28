emailto=['tamil@yopmail.com']  # Provide an Toemail address where the report need to be sent.You can also provide any number of To eamil address For example: ['tamil@yopmail.com','sensor@yopmail.com']





emailfrom='patchreport1@gmail.com'
password='Patchreport@123'
smtpserver='smtp.gmail.com'
port=587

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
import shutil
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
    print a
    find=re.findall('SpmAgent.*',c)
    print find
    sc=os.path.join(a,find[0])
    ds=os.path.join(os.environ['ProgramData'],'log_report.txt')
    try:
        os.chmod(sc,0644)
        os.chmod(ds,0644)
    except:
        pass
    if find:
        shutil.copy(sc,ds)
    else:
        print 'There is no SPM LOGS'
    return ds

if 'PROGRAMFILES(X86)' in os.environ.keys():
    pmlpath=os.path.join(os.environ['PROGRAMFILES(X86)'], 'COMODO\\Comodo ITSM\\spmlogs')
else:
    pmlpath=os.path.join(os.environ['PROGRAMFILES'], 'COMODO\\Comodo ITSM\\spmlogs')
    

s=getrmm(pmlpath)
subject='%s %s SPM Logs report'%(computername(), ipaddress())

fileToSend=s

if sendmail==1:
    print emailreport(subject,emailto,emailfrom,fileToSend,password,smtpserver,port,msgbody)
    print 'mail send'
else:
    print " Set sendmail value as 1 "

