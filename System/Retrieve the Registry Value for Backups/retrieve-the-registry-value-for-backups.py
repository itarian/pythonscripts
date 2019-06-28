emailto='xyz@gmail.com'# Provide a valid email for sending the alert details.
#For Example, emailto= yyy@gmail.com
sendmail=1## [1 sends mail or 0 does not send mail] 	
import os
import ctypes
import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

emailfrom=r'reportbackupinfo@gmail.com'     
password='Backup@123'
smtpserver='smtp.gmail.com'             
port=587                     

msgbody=r'''
Hi

Please find the attachment which retrieve a registry value for backup in Text file format.

Thank you.
'''
import socket
ip=socket.gethostbyname(socket.gethostname())
name=os.environ['username']
print 'PC-NAME : '+name
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print "IP-ADDRESS : " + (s.getsockname()[0])
fileToSend1=os.path.join(os.environ['ProgramData'],'report.txt')
subject="registry value backup - reg"

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
    msg["To"] = emailto
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
        return "The email report has been sent to "+msg["To"]
    
    except Exception as e:
        return e
    
with disable_file_system_redirection():
    cmd=r"reg query HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\BackupRestore /s"
    a=os.popen(cmd).read()
    if a:
        with open(fileToSend1,"w")as f:
            f.write('PC-NAME : '+name+"\n")
            f.write("IP-ADDRESS : " + (s.getsockname()[0]) +"\n")
            f.write(a)
            f.close()
    else:
        print "No back up values has been retrieved"
        sendmail=0
if sendmail==1:
    print emailreport(subject,emailto,emailfrom,fileToSend1,password,smtpserver,port,msgbody)

def remove():
    try:
        os.remove(fileToSend1)
    except:
        pass
remove()
