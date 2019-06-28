emailto=['xxxxxx@gmail.com']  # Provide an Toemail address where the report need to be sent.You can also provide any number of To eamil address For example: ['tamil@yopmail.com','sensor@yopmail.com']

emailfrom='yyyyyyyyyyy'
password='**********'
smtpserver='smtp.gmail.com'
port=587

sendmail=1 ## [1 sends mail or 0 does not send mail] if sendmail=1 then user have to set the required information to send out a email from the code.
msgbody=r'''Hi

Please find the attachment for thePassword expiry report of all the Active directory Users report in Text file format.

Thank you.'''

import os
import re
import ctypes
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

fileToSend1=os.path.join(os.environ['ProgramData'],'password_expiry_details.txt')

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
    

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

def write(c):
    with open(fileToSend1, 'a') as f:
        f.write(c)


with disable_file_system_redirection():
    v="password expires"
    path="C:\output.txt"
    
    os.popen("dsquery user | dsget user -samid > "+path).read()
    x=[]
    x = [line.strip() for line in open(path, 'r')]
    print "The Active directory users and their password expiry dates"
    for i in range (len(x)-1):
        print x[i]
        write(x[i])
        write('\n')
        cmd="net user "+x[i]+" /domain >"+path
        a=os.popen(cmd).read()
        if  os.path.exists(path):    
            with open (path, 'r') as file:
                for line in file:
                        string=''
                        string1=''
                        string2=''
                        line=line.strip()
                        if 'Password expires' in line:
                            if 'Never' in line:
                                string2+=''.join(line)
                                print string2
                                print "\n"
                                write(string2)
                                write('\n')
                                write('\n')
                            else:
                                line=line.strip()
                                string+=''.join(line)
                                time3=re.findall('Password expires\s\s\s\s\s\s\s\s\s\s\s\s (.*)',string)
                                string1+=''.join(time3)
                                up_time=string1.split(' ')[0]
                                p=up_time.split('/')[0]
                                q=up_time.split('/')[1]
                                r=up_time.split('/')[2]
                                p1=int(p)
                                q1=int(q)
                                r1=int(r)
                                import datetime
                                cur_time=datetime.datetime.now()
                                cur_time1=cur_time.strftime("%d-%m-%Y")
                                p2=cur_time1.split('-')[0]
                                q2=cur_time1.split('-')[1]
                                r2=cur_time1.split('-')[2]
                                p2=int(p2)
                                q2=int(q2)
                                r2=int(r2)
                                ass=datetime.date(r2,q2,p2) - datetime.date(r1,p1,q1)
                                if ass==-2:
                                    print x[i]+" - Your Password will expire within 2 days"
                                    write(x[i]+" - Your Password will expire within 2 days")
                                else:
                                    print x[i]+" - Your Password will expiries at "+up_time
                                    write(x[i]+" - Your Password will expiries at "+up_time)
                                write('\n')
                                write('\n')
                                print "\n"
                                
subject='%s %s Password expiry report of all the Active directory Users report'%(computername(), ipaddress())

fileToSend=fileToSend1

if sendmail==1:
    print emailreport(subject,emailto,emailfrom,fileToSend,password,smtpserver,port,msgbody)
    print 'mail sent '
else:
    print " Set sendmail value as 1 "
	
if os.path.exists(fileToSend1):
	os.remove(fileToSend1)
