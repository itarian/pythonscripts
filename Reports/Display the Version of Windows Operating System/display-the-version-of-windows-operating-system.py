emailto=['pandi@yopmail.com']  # Provide an Toemail address where the report need to be sent.You can also provide any number of To eamil address For example: ['pandi@yopmail.com','sensor@yopmail.com']
emailfrom='coneoperations@gmail.com' # Provide from email address
password='*********' # Provide Password
smtpserver='smtp.gmail.com'
port=587



import subprocess
from subprocess import PIPE, Popen
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

dev_name=os.environ['computername']
ip_add=socket.gethostbyname(socket.gethostname())

msgbody=r'''Hi

Please find the attachment for the Windows OS Details as Text file format.

Thank you.'''

subject='%s %s OS Details report'%(ip_add, dev_name)

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
    

obj = subprocess.Popen('systeminfo | findstr OS', shell = True, stdout = PIPE, stderr = PIPE)
out, err = obj.communicate()
if err:
    print "Error getting OS Details"
elif out:
    fp=os.path.join(os.environ['ProgramData'],"OS_Details.txt")
    with open(fp,'w+') as f:
        f.write("IP address : "+ip_add+"\n")
        f.write("Device Name : "+dev_name+"\n")
        f.write('\n'+'\n')
        f.write(out)
    if os.path.isfile(fp):
        fileToSend=fp
        print emailreport(subject, emailto,emailfrom,fileToSend,password,smtpserver,port,msgbody)
