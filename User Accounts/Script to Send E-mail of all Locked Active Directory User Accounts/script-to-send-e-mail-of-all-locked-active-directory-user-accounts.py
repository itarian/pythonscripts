import re

ps_content=r'''

Get-ADUser -Filter * | Select-Object Name | ft -HideTableHeaders

'''
def lock(user):
    ps_content1=r'''

    Get-ADUser %s -Properties * | Select-Object LockedOut

    '''%user
    return ps_content1
import os

def ecmd(command):
    import ctypes
    from subprocess import PIPE, Popen
    
    class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
    
    with disable_file_system_redirection():
        obj = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()
    ret=obj.returncode
    if ret==0:
        if out:
            return out.strip()
        else:
            return ret
    else:
        if err:
            return err.strip()
        else:
            return ret

file_name='powershell_file.ps1'
file_path=os.path.join(os.environ['TEMP'], file_name)
with open(file_path, 'wb') as wr:
    wr.write(ps_content)

ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
k=ecmd('powershell "%s"'%file_path)
k=re.sub("\s+", ",", k.strip())
k=k.replace(","," ")
k=k.split(" ")
c=0
fi=[]
for user in k:
    ps_content=lock(user)
    file_name='powershell_file1.ps1'
    file_path=os.path.join(os.environ['TEMP'], file_name)
    with open(file_path, 'wb') as wr:
        wr.write(ps_content)
    ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
    ki=ecmd('powershell "%s"'%file_path)
    ki=str(ki)
    
    if "True" in ki:
        
        ap=user+" Account is  locked"
        fi.append(ap)
        c=c+1
        
    elif ki=="0":
        kk=0
        
    else:
        kkk=0
        

os.remove(file_path)


if c>1:
    fi="\n".join(fi)
   
else:
    fi="No active directory user accounts lockedout at this moment"


emailto='xxxxxxxx@YYYYY' #E-mail To
emailfrom='XXXXXXX1@gmail.com' #Give your from addrees
password='XXXXXXXXX' #Password
smtpserver='smtp.gmail.com'
port=587
import os
import subprocess
import shutil,urllib2,time
from subprocess import PIPE, Popen
import socket
import smtplib
import mimetypes
import ctypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from subprocess import PIPE, Popen
import _winreg

def emailreport(subject, emailto,emailfrom,password,smtpserver,port,msgbody):
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = "".join(emailto)
    msg["Subject"] = subject
    msg.preamble = subject
    body = MIMEText(msgbody)
    msg.attach(body)       
    try:
        server = smtplib.SMTP(smtpserver,port)
        server.ehlo()
        server.starttls()
        server.login(emailfrom, password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
        return "The email report has been sent to "+msg["To"]
    except Exception as e:
        return e
def Email(emailto,emailfrom,password,smtpserver,port):
   
    msgbody=r'''
    Hi

    Please find the Active directory user accounts which are locked

    %s

    Thank you.
    '''%fi
    emailto=emailto
    emailfrom=emailfrom
    password=password
    smtpserver=smtpserver
    port=port
    subject=' Alldevices report'
    print emailreport(subject,emailto,emailfrom,password,smtpserver,port,msgbody)

Email(emailto,emailfrom,password,smtpserver,port)

