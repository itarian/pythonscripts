emailto='xxx@gmail.com' #Provide a valid email for sending the alert details.
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
import time
import sys
import ssl
import sys
import ctypes
from datetime import datetime
emailfrom='windowsbackupreport@gmail.com'     
password='Backup@123'	        
smtpserver='smtp.gmail.com'            
port=587                    
sendmail=1 ## [1 sends mail or 0 does not send mail] if sendmail=1 then user have to set the required information to send out a email from the code.
msgbody=r'''
Hi

Please find the attachment for the custom backup in server Text file format.

Thank you.
'''

def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

def emailreport(subject, emailto,emailfrom,fileToSend,password,smtpserver,port,msgbody):
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = "".join(emailto)
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
        server.login(emailfrom,password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
        return " \n The email report has been sent to "+msg["To"]
    
    except Exception as e:
        
        return e

ab=0
ac=0
date_format = "%Y-%m-%d"
time_now=time.strftime('%Y-%m-%d')
a = datetime.strptime(time_now, date_format)
x=os.popen('wevtutil qe Microsoft-Windows-Backup /f:text /q:*[System/EventID=8]   /rd:true').read()
y=os.popen('wevtutil qe Microsoft-Windows-Backup /f:text /q:*[System/EventID=4]   /rd:true').read()
Name=[i.strip() for i in  x.split("\n") if i.strip()]
Profile=Name[1:]
b=[]
for k in Profile:
    sam2=re.findall('Date:(.*)',k)
    i1=''.join(sam2)
    b.append(i1+' ')
Name1=[i.strip() for i in  y.split("\n") if i.strip()]
Profile1=Name1[1:]
a1=[]
for k1 in Profile1:
    sam3=re.findall('Date:(.*)',k1)
    i3=''.join(sam3)
    a1.append(i3+' ')
fileToSend=os.path.join(os.environ['TEMP'],'report.txt')
iu=''.join(a1)
iv=''.join(b)
name=os.environ['username']
print 'PC-NAME:' +name
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
print "IP-ADDRESS : " + (s.getsockname()[0])
def cancel():
    ac=0
    if re.findall("canceled",x):
        for j in Profile:
            o=re.findall('Date: (.*)T',j)
            i=''.join(o)
            if i=='':
                pass
            else:
               a1 = datetime.strptime(i, date_format)
               if a1!=a:
                   ac=ac+1  
               else:
                   ac=0             
    return ac
                          
def success():
    ab=0
    if re.findall("successfully",y):
        for j1 in Profile1:
            o1=re.findall('Date: (.*)T',j1)
            i4=''.join(o1)
            if i4=='':
                pass
            else:
               a2 = datetime.strptime(i4, date_format)
               if a2!=a:
                   ab=ab+1
                   
               else:
                   ab=0
    return ab
k=os.popen('wevtutil qe Microsoft-Windows-Backup /f:text /q:*[System/EventID=14]   /rd:true').read()
s1=re.findall('Date:(.*)',k)
u=''.join(s1)
if re.findall("completed",k):
    ap=cancel()
    au=success()
    if ap>0 and au>0:
        print "The Backup Operation was canceled at " + iv + '\n' 
        print "The Backup Operation was Success at" + iu + '\n'
        with open(fileToSend, 'w') as f:
            f.write('PC-NAME : '+name + '\n')
            f.write("IP-ADDRESS : " + (s.getsockname()[0]))
            f.write("The Backup Operation was canceled at " + iv)
            f.write("The Backup Operation was Success at" + iu)
            
        alert(1)
    elif au==1 and ap==0:
        
        print  "The Backup Operation was Success at" + iu + '\n'
        with open(fileToSend, 'w') as f:
            f.write('PC-NAME : '+name + '\n')
            #f.write("IP-ADDRESS : " + (s.getsockname()[0]))
            print "IP-ADDRESS : " + (s.getsockname()[0])
            f.write("The Backup Operation was Success at " + iu)
            
        alert(1)
    elif ap==1 and au==0:
        
        print  "The Backup Operation was canceled at" + iv + '\n'
        with open(fileToSend, 'w') as f:
            f.write('PC-NAME : '+name + '\n')
            f.write("IP-ADDRESS : " + (s.getsockname()[0]) + '\n')
            f.write("The Backup Operation was canceled at ort has bee" + iv)
            
        alert(1)
        
    elif ap==0 and au==0:
        print "The Last Backup Operation at " + u
        with open(fileToSend, 'w') as f:
            f.write('PC-NAME : '+name + '\n')
            f.write("IP-ADDRESS : " + (s.getsockname()[0]) + '\n')
            f.write("The Last Backup Operation at " + u)
            
        alert(0)
        
    else:
        print "No Backup operation occur"
        with open(fileToSend, 'w') as f:
            f.write('PC-NAME : '+name + '\n')
            f.write("IP-ADDRESS : " + (s.getsockname()[0]) + '\n')
            f.write("No Backup Operation Occur")
        alert(0)
   
subject='Custom backup report'
if sendmail==1:
    print emailreport(subject,emailto,emailfrom,fileToSend,password,smtpserver,port,msgbody)
else:
    print " Set sendmail value as 1"

