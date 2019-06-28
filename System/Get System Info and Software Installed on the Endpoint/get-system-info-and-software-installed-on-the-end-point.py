sendmail=1 ## [1 sends mail or 0 does not send mail] if sendmail=1 then user have to set the required information to send out a email from the code.
msgbody='Hi,\n\nPlease find the attachment for System Information and Instlled Software List.\n\nThank you.'
emailto=['xxx@gmail.com']#E-mail To 
emailfrom='yyy@gmail.com'#Give your from addrees
password='zzzzzzz'#Password
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
        return " "+msg["To"]
    except Exception as e:
        return e
##FUNCTION  TO EDIT CSV FILE
def csvedit(str23):
    list=[]
    li=[]
    for i,c in enumerate(str23):
        if ":"==c:
            li.append(i)
        

    if len(li)>0:
        for i in range(1,len(li)):
            
            str23=  str23[:li[i]]+'|'+ str23[li[i]+1:]
        return str23
#FUNCTION TO GET SYSTEM INFO
def Systeminfo():
    
    a.append( "\nSYSTEM INFO\n")
    ki=os.popen('systeminfo').read()
    space=ki.replace(' ', '')
    space1=space.split('\n')
    for j in space1:
        sam=j
        a.append(csvedit(sam))
    global str1
    str1= '\n'.join(str(e) for e in a)
    
def collectprograms(rtkey,pK,kA):
    import _winreg
    import os
    list=[]
    oK=_winreg.OpenKey(rtkey,pK,0,kA)
    i=0
    while True:
        try:
            bkey=_winreg.EnumKey(oK,i)
            vkey=os.path.join(pK,bkey)
            oK1=_winreg.OpenKey(rtkey,vkey,0,kA)
            try:
                DN,bla=_winreg.QueryValueEx(oK1,'DisplayName')
                DV,bla=_winreg.QueryValueEx(oK1,'DisplayVersion')
                inlist=[DN.strip(), DV.strip()]
                if inlist[1]=="None":
                    gh=0
                else:
                    ki="\n"+inlist[0]+" "+inlist[1]+"\n"
                    b.append(ki)
                    global str2
                    str2 = ''.join(str(e) for e in b)
                    
            except:
                pass
            i+=1
        except:
            break
    _winreg.CloseKey(oK)

def programsinstalled():
    uninstallkey='SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'
    if 'PROGRAMFILES(X86)' in os.environ.keys():
        rklist=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ),
                (_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ),
                (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ),
                (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ)]
    else:
        rklist=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_READ),
                (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_READ)]
    collected=''
    uninstalled=''
    error=''
    blacklisted=''
    hasnoss=[]
    ic=0
    uc=0
    ec=0
    for i in rklist:
        col=collectprograms(i[0], i[1], i[2])

Systeminfo()
INST=("\nINSTALLED SOFTWARE  LIST\n")
programsinstalled()

temp=os.environ['TEMP']
cf=os.path.join(temp, 'InstalledInfo.csv')
with open(cf, "w") as myfile:
    myfile.write("%s\n" % str1)
    myfile.write(INST)
    myfile.write("%s\n" % str2)


fileToSend=os.path.join(os.environ['TEMP'], 'Installedinfo.csv')
subject='%s %s  Report CSV'%(computername(), ipaddress())
if sendmail==1:
    print "email has been sent to" + emailreport(subject, emailto,emailfrom,fileToSend,password,smtpserver,port,msgbody)
else:
    with open(fileToSend) as fr:
        print fr.read().replace('|', '  ')
