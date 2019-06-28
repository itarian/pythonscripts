sendmail=1## [0 sends mail or 1 does not send mail] if sendmail=1 then user have to set the required information to send out a email from the code.
import os
import ctypes
global c
c=0
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
msgbody='Hi,\n\nPlease find the attachment for Event Logs .\n\nThank you.'
emailto=['xxxxxxxx@YYYYY']#E-mail To 
emailfrom='XXXXXXX1@gmail.com'#Give your from addrees
password='XXXXXXXXX'#Password
smtpserver='smtp.gmail.com'
import os,sys,csv,urllib2,zipfile,shutil,re,sys,socket,_winreg,random,getpass
import xml.etree.ElementTree as ET
a=[]
b=[]
c=[]
print "USER NAME: "+getpass.getuser()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print "IP-ADDRESS : "+(s.getsockname()[0])
from time import gmtime, strftime
time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
port=587
def computername():
    import os
    return os.environ['COMPUTERNAME']

## get ip address
def ipaddress():
    import socket
    return socket.gethostbyname(socket.gethostname())
## function to email with attachment
def emailreport(subject, emailto,emailfrom,password,smtpserver,port,msgbody):
    if c==0:
        files=["Securitylogs.txt","Applicationlogs.txt","Setuplogs.txt","Systemlogs.txt"]
        files.append('Forwardedevents.txt')
    else:
        files=["Securitylogs.txt","Applicationlogs.txt","Setuplogs.txt","Systemlogs.txt"]       
    
    import smtplib
    import mimetypes
    from email.mime.multipart import MIMEMultipart
    from email import encoders
    from email.message import Message
    from email.mime.audio import MIMEAudio
    from email.mime.base import MIMEBase
    from email.mime.image import MIMEImage
    from email.mime.text import MIMEText
    import os
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = ",".join(emailto)
    msg["Subject"] = subject
    msg.preamble = subject
    body = MIMEText(msgbody)
    msg.attach(body)      
    for f in files:
        with open(f, 'rb') as fp:
            record = MIMEBase('text', 'octet-stream')
            record.set_payload(fp.read())
            encoders.encode_base64(record)
            record.add_header('Content-Disposition', 'attachment', filename=os.path.basename(f))
            msg.attach(record)
    try:
        server = smtplib.SMTP(smtpserver,port)
        server.ehlo()
        server.starttls()
        server.login(emailfrom, password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
        return " "+msg["To"]
    except Exception as e:
        return e
#FUNCTION TO GET SYSTEM INFO
with disable_file_system_redirection():
    applogs=os.popen('wevtutil qe Security /f:text /c:10 /rd:True"').read()
    sam1=applogs
    applogs1=os.popen('wevtutil qe Application /f:text /c:10 /rd:True"').read()
    sam2=applogs1
    applogs2=os.popen('wevtutil qe Setup /f:text /c:10 /rd:True"').read()
    sam3=applogs2
    applogs3=os.popen('wevtutil qe System  /f:text /c:10 /rd:True"').read()
    sam4=applogs3
    applogs4=os.popen("wevtutil qe ForwardedEvents  /f:text /c:10 /rd:True").read()
    sam5=applogs4
temp=os.environ['TEMP']
os.chdir(temp)
global cf1
global cf2
global cf3
global cf4

cf1=os.path.join(temp, 'Securitylogs.txt')
cf2=os.path.join(temp, 'Applicationlogs.txt')
cf3=os.path.join(temp, 'Setuplogs.txt')
cf4=os.path.join(temp, 'Systemlogs.txt')
if len(sam5)!=0:
	global cf5
	cf5=os.path.join(temp, 'Forwardedevents.txt')
	with open(cf5, "w") as myfile:
		myfile.write("***********\nForwarded  Events\n**********\n")
		myfile.write(sam5)
else:
    c=1
    
with open(cf1, "w") as myfile:
    myfile.write("***********\nSECURITY LOGS\n**********\n")
    myfile.write(sam1)
with open(cf2, "w") as myfile:
	myfile.write("***********\nAPPLICATION LOGS\n***********\n")
	myfile.write(sam2)
with open(cf3, "w") as myfile:
	myfile.write("***********\nSETUP LOGS\n***********\n")
	myfile.write(sam3)
with open(cf4, "w") as myfile:
	myfile.write("***********\nSYSTEM LOGS\n***********\n")
	myfile.write(sam4)

subject='%s %s  Event Logs'%(computername(), ipaddress())
if sendmail==0:
    print "Event Logs has sent to Email with  " + emailreport(subject,emailto,emailfrom,password,smtpserver,port,msgbody)
else:
	if c==0:
		files=["Securitylogs.txt","Applicationlogs.txt","Setuplogs.txt","Systemlogs.txt"]
		files.append('Forwardedevents.txt')
	else:
		files=["Securitylogs.txt","Applicationlogs.txt","Setuplogs.txt","Systemlogs.txt"]
	for f in files:
		with open(f) as fr:
			print fr.read().replace('|', '  ')
