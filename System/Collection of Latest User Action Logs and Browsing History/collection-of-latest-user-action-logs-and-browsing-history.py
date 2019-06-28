import xml.etree.ElementTree as ET
import getpass
import socket
import _winreg
import os
import subprocess
import ctypes
import re
import sys
import time
import smtplib
import zipfile
import shutil
import random
import urllib2

import xml.etree.ElementTree as ET
print "USER NAME: "+getpass.getuser()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print "IP-ADDRESS : "+(s.getsockname()[0])
from time import gmtime, strftime
time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
sendmail=1 ## [1 sends mail or 0 does not send mail] if sendmail=1 then user have to set the required information to send out a email from the code.
msgbody='Hi,\n\nPlease find the attachment for User accessed settings details and browser history for last 48 hours.\n\nThank you.'
emailto=['xxxx@gmail.com']#E-mail To 
emailfrom='yyyy@gmail.com'#Give your from addrees
password='zzzzzzzzzz'#Password
smtpserver='smtp.gmail.com'
port=587


## get computer name
def computername():
    import os
    return os.environ['COMPUTERNAME']

## get ip address
def ipaddress():
    import socket
    return socket.gethostbyname(socket.gethostname())

## function to email with attachment
def emailreport(subject, emailto,emailfrom,fileToSend,password,smtpserver,port,msgbody):
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
        return "User accessed settings details and browser history for last 48 hours  has been sent over email to "+msg["To"]
    except Exception as e:
        return e


def ecmd(CMD, r=False):
    import ctypes
    class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
    from subprocess import PIPE, Popen
    with disable_file_system_redirection():
        OBJ = Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = OBJ.communicate()
    ret=OBJ.returncode
    if r:
        return ret
    else:            
        if ret==0:
            return out
        else:
            return ret

if 'PROGRAMW6432' in os.environ.keys():
    url='http://www.nirsoft.net/utils/browsinghistoryview-x64.zip'
else:
    url='http://www.nirsoft.net/utils/browsinghistoryview.zip'

req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
con = urllib2.urlopen(req)

    
temp=os.environ['APPDATA']
zf=os.path.join(temp, url.split('/')[-1])
with open(zf, 'wb') as w:
      chunk=con.read(100*1000*1000)
      if chunk:
          w.write(chunk)
      else:
          sys.exit()
z=zipfile.ZipFile(zf, 'r')
ep=os.path.join(temp, url.split('/')[-1][:-4])
z.extractall(ep)
z.close()
os.remove(zf)
if os.path.exists(ep):
    pf=os.path.join(ep, 'BrowsingHistoryView.exe')
    if os.path.isfile(pf):
        cf=os.path.join(temp, 'browsinghistory.csv')
        ec=ecmd('"%s" /scomma "%s"'%(pf, cf), r=True)
        if ec==0:
            print 'Report has been created........'
            histroy=open(cf).read()
##            print type(histroy)
            
        else:
            print ec, 'error on report creation'
else:
    print 'error on extraction ...'

print '\n'
event_logs=os.popen('wevtutil qe Security /f:text /c:20 /rd:True ').read()
reg_log=re.findall('Event\sID:\s46[0-9]{2}',event_logs)
get_reg,ale=0,0
get_reg1=0
get_reg2=0
a=[]
b=[]
c=[]
for id in reg_log:
    if id=='Event ID: 4672':
        get_reg=get_reg+1
    elif id=='Event ID: 4688':
        get_reg1=get_reg1+1
    elif id=='Event ID: 4648':
        get_reg2=get_reg2+1


if get_reg>0:
    a.append("1.UAC AUTHOURIZED TO THE LOGON USER")
    event_logs1=os.popen('wevtutil qe Security /f:xml /c:20 /rd:True |findstr ="Event ID: 4672"').read()
    k=re.search('<System>.*<?System>',event_logs1)
    k=k.group()
    a.append("Here are the following details with EVENT ID :")
    xml = ET.fromstring(k)
    for i in xml.getchildren():
        if i.attrib != {}:
            a.append(i.tag)
            a.append(i.attrib)
        else:
            if i.text is not None:
                a.append(i.tag)
                a.append(i.text)
else:
        a.append("1.NO UAC AUTHOURIZED TO THE LOGON USER")

if get_reg1>0:
        b.append("2: A new process has been created/recorded in the audit process tracking")
        event_logs2=os.popen('wevtutil qe Security /f:xml /c:20 /rd:True |findstr ="Event ID: 4688"').read()
        k=re.search('<System>.*<?System>',event_logs2)
        k=k.group()
        b.append("Here are the following  Audit Process Tracking details with  coressponding EVENT ID:")
        xml = ET.fromstring(k)
        for i in xml.getchildren():
            if i.attrib != {}:
                    b.append(i.tag)
                    b.append(i.attrib)
            else:
                if i.text is not None:
                    b.append(i.tag)
                    b.append(i.text) 
else:
        b.append("2: NO,A new process has been created/recorded in the audit process tracking")       

if get_reg2>0:
    c.append("3: Usage of user account with admin rights")
    event_logs3=os.popen('wevtutil qe Security /f:xml /c:20 /rd:True |findstr ="Event ID: 4648"').read()
    k=re.search('<System>.*<?System>',event_logs3)
    k=k.group()
    c.append("Here are the following details with EVENT ID :")
    xml = ET.fromstring(k)
    for i in xml.getchildren():
        if i.attrib != {}:
            c.append(i.tag)
            c.append(i.attrib)
        else:
            if i.text is not None:
                c.append(i.tag)
                c.append(i.text) 
else:
        c.append("3: NO,Usage of user account with admin rights")         

with open(cf, "a") as myfile:
    myfile.write("%s\n" % a)
    myfile.write("%s\n" % b)
    myfile.write("%s\n" % c)

fileToSend=os.path.join(os.environ['APPDATA'], 'browsinghistory.csv')
subject='%s %s  Report CSV'%(computername(), ipaddress())
if sendmail==1:
    print emailreport(subject,emailto,emailfrom,fileToSend,password,smtpserver,port,msgbody)
else:
    with open(fileToSend) as fr:
        print fr.read().replace('|', '  ')
