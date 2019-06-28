emailto=['xxx@gmail.com'] # Provide a valid email for sending the alert details.
#For Example, emailto= [yyy@gmail.com, zzz@gmail.com]
sendmail=1 ## [1 sends mail or 0 does not send mail] if sendmail=1 then user have to set the required information to send out a email from the code.	
import os
import sys
import time
import ssl
import sys
import ctypes
import filecmp
import difflib
import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import re
from datetime import datetime
emailfrom=r'reportbackupinfo@gmail.com'     
password='Backup@123'
smtpserver='smtp.gmail.com'             
port=587                     

msgbody=r'''
Hi

Please find the attachment for the custom backup in server Text file format.

Thank you.
'''
flag =0
import socket
ip=socket.gethostbyname(socket.gethostname())

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
        server.login(emailfrom,password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
        return " \n The email report has been sent to "+msg["To"]
    
    except Exception as e:
        return e


class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
fileToSend1=os.path.join(os.environ['ProgramData'],'report.txt')
fileToSend2=os.path.join(os.environ['ProgramData'],'report_new.txt')
save_path=os.environ['ProgramData']
date_format = "%Y-%m-%d"
def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))


r=0
def write(c):
    fn="report.txt"
    fn1='report_new.txt'
    if os.path.exists(fileToSend1):
        with open(fileToSend2, 'w+') as f:
                f.write("IP-ADDRESS : " +ip+'\n')
                f.write(c)
               
    else:
        with open(fileToSend1, 'w+') as f:
                f.write("IP-ADDRESS : " +ip+'\n')
                f.write(c)
                
    if not os.path.exists(fileToSend2):
        with open(fileToSend1, 'w+') as f:
                f.write("IP-ADDRESS : " +ip+'\n')
                f.write(c)
def check():
    f1=fileToSend1
    f2=fileToSend2
    f=0
    if False==0:
        with open(f1) as file:
           data=file.read()
           data.strip()
           with open(f2) as file:
               data2=file.read()
               data2.strip()
               text1Lines = data.splitlines(1)
               text2Lines = data2.splitlines(1)
               diffInstance = difflib.Differ()
               diffList = list(diffInstance.compare(text1Lines,text2Lines ))
               for line in diffList:
                   if line.startswith('+') or line.startswith('-'):
                       f=1
                   
           file.close()
        file.close()
    return f



def remove():
    os.remove(fileToSend1)
    os.rename(fileToSend2,fileToSend1)
 

import datetime
cd1=datetime.datetime.now()
cd=cd1.strftime("%Y-%m-%d")
with disable_file_system_redirection():
    cmd=os.popen('wevtutil qe Microsoft-Windows-Backup /f:text /q:*[System/EventID=4]   /rd:true /c:1').read()
    cmd1=os.popen('wevtutil qe Microsoft-Windows-Backup /f:text /q:*[System/EventID=8]   /rd:true /c:1').read()
    cmd2=os.popen('wevtutil qe Microsoft-Windows-Backup /f:text /q:*[System/EventID=1]   /rd:true /c:1').read()

fg=0
if re.findall("started",cmd2):
    time=re.findall('Date:(.*)',cmd2)[0]
    d=time.split('T')[0].strip()
    if d==cd:   
        if re.findall("finished successfully",cmd):
            time1=re.findall('Date:(.*)',cmd)[0]
            if time1 > time:
                    write(cmd)
                    s=check()
                    fg=1

            elif re.findall("canceled",cmd1):
                time2=re.findall('Date:(.*)',cmd1)[0]
                if time2 > time:
                    write(cmd1)
                    s=check()
                    fg=0
                    
            
    else:
        with open(fileToSend1, 'w') as f:
            f.write("IP-ADDRESS : " +ip+'\n')
            f.write('There is No Backup operation has started Today  ')
        s=0
        r=1

else:
    with open(fileToSend1, 'w') as f:
        f.write("IP-ADDRESS : " +ip+'\n')
        f.write('There is No Backup operation occur in the System')
    s=0
    r=1


if s==1:
    print "Backup operation occured in the System.You need to check your mail for the status of the backup whether it is success or fail"
    sendmail=1
    alert(1)
else:
    print "Currently there is no backup operation occured in this System"
    alert(0)
    sendmail=0

if fg==0:
    subject='Report for backup is failure'
    
elif fg == 1:
    subject='Report for backup is success'
    

if r==0:
    remove()
if sendmail==1:
    print emailreport(subject,emailto,emailfrom,fileToSend1,password,smtpserver,port,msgbody)

