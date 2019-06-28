URL='http://download.piriform.com/ccsetup523.exe' #give the direct download link of the software to be downloaded
sCMD='/S' #give the silent installation command 
AppName = "CCleaner"  #give the name of the applicaiton as in control panel

emailto=['XXX@gmail.com']#E-mail To 
emailfrom='YYY@gmail.com'#Give your from addrees
password='ZZZ'#Password

import os
import ctypes
global c
import urllib
c=0

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
path = os.environ['TEMP']



class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


def computername():
    import os
    return os.environ['COMPUTERNAME']

## get ip address
def ipaddress():
    import socket
    return socket.gethostbyname(socket.gethostname())

def install(path,URL,sCMD) :
    if os.path.exists(path):
        fn = URL.split('/')[-1]
        fp = os.path.join(path, fn)
        try:
            with open(fp, 'wb') as f:
                try:
                    f.write(urllib.urlopen(URL).read())
                    print fp
                except Exception as e:
                    print e
        except Exception as e:
            print e
        try:
            install = os.popen(fp+' '+sCMD).read()
            return  'Great!'+ 'Successfully Installed'
        except Exception as e:
            return e
        os.chdir(path)
        os.remove(fn)
    else:
        return 'No path: '+path+' is exist'

print install(path,URL,sCMD)


## function to email with attachment
def emailreport(subject, emailto,emailfrom,password,smtpserver,port,msgbody):
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

def CheckApp(AppName):
    import _winreg
    import os
    AppName = AppName.lower()
    def DNDS(rtkey, pK, kA):
        ln = []
        lv = []
        try:
            oK = _winreg.OpenKey(rtkey, pK, 0, kA)
            i = 0
            while True:
                try:
                    bkey = _winreg.EnumKey(oK, i)
                    vkey = os.path.join(pK, bkey)
                    oK1 = _winreg.OpenKey(rtkey, vkey, 0, kA)
                    try:
                        tls = []
                        DN, bla = _winreg.QueryValueEx(oK1, 'DisplayName')
                        DV, bla = _winreg.QueryValueEx(oK1, 'DisplayVersion')
                        _winreg.CloseKey(oK1)
                        ln.append(DN)
                        lv.append(DV)
                    except:
                        pass
                    i += 1
                except:
                    break
            _winreg.CloseKey(oK)
            return zip(ln, lv)
        except:
            return zip(ln, lv)
 
    rK = _winreg.HKEY_LOCAL_MACHINE
    sK = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
    openedKey = _winreg.OpenKey(rK, sK, 0, _winreg.KEY_READ)
    arch, bla = _winreg.QueryValueEx(openedKey, 'PROCESSOR_ARCHITECTURE')
    arch = str(arch)
    _winreg.CloseKey(openedKey)
 
    if arch == 'AMD64':
        fList = DNDS(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_32KEY | _winreg.KEY_READ)
        fList.extend(DNDS(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_64KEY | _winreg.KEY_READ))
        fList.extend(DNDS(_winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_32KEY | _winreg.KEY_READ))
        fList.extend(DNDS(_winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_64KEY | _winreg.KEY_READ))
    else:
        fList = DNDS(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_READ)
        fList.extend(DNDS(_winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_READ))
    fList = set(fList)
 
    lr = []
    rs = 0
    for i in fList:
        a, b = i
        if AppName in a.lower():
            lr.append('success: {} is installed'.format(a))
            lr.append('{:<25}{:5}'.format(a, b))
            rs += 1
        else:
            rs += 0
    if rs:
        return "True"   
    else:
        return "False"
        
if CheckApp(AppName):
    msgbody = "The application "+AppName + " installed successfully"
    sendmail=1
else:
    print  "The application is not installed or not found"
    sendmail=0

subject   ='%s %s'%(computername(), ipaddress())
if sendmail==1:
    mail = emailreport(subject,emailto,emailfrom,password,smtpserver,port,msgbody)
    print "The successful installation status has been to"
    print mail

