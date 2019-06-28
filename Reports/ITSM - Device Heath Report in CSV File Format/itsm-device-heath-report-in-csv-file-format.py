emailto=['abc@yopmail.com']      # Provide an email where want to send CSV file.
emailfrom='xyze@gmail.com'        # Provide a valide from email.
password='*****'	         # Provide the correct password for your from mail.
smtpserver='smtp.gmail.com'
port=587

sendmail=0 ## [1 sends mail or 0 does not send mail] if sendmail=1 then user have to set the required information to send out a email from the code.
msgbody=r'''Hi

Please find the attachment for the Computer Health Report in CSV file format.

Thank you.'''




e=[]
b=[]
d="Rmm_dll"
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
        return "the email report has been sent to "+msg["To"]
    except Exception as e:
        return e

def ecmd(CMD):
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
    return out.strip()

def getrmm(a):
    os.chdir(a)
    c=os.popen("dir").read()
    find=re.findall('Rmm_dll(.*)',c)

    for i in find:
        b.append(a+'\\'+d+i)

            
    for i in b:
        with open (i, 'r+') as file:
            for line in file:
                string=''
                line=line.strip()
                if line.startswith('name:') or  line.endswith('PROCEDURE_FINISHED_SUCCESS') or line.endswith('PROCEDURE_STARTED') or line.endswith('PROCEDURE_FINISHED_FAIL') or line.endswith('Proto message was parsed successfully'):
                        line=line+'\n'
                        string+=line
                        e.append(string)


    
def procedure(string):
    alist=re.findall('name:.*\n\[INFO\].*', string)
    procedure_name=[]
    for i in alist:
        ilist=i.split('\n')
        name=ilist[0].split(':')[1].strip().replace('"', '')
        if name not in procedure_name:
            procedure_name.append(name)
    
    return procedure_name

temp=str(random.randint(2017, 3000))+'.txt'
ptemp=str(random.randint(2017, 3000))+'p.txt'
if 'PROGRAMFILES(X86)' in os.environ.keys():
    if os.path.exists(os.path.join(os.environ['PROGRAMFILES(X86)'], 'COMODO\Comodo ITSM\cpmlogs')):
        pmlpath=os.path.join(os.environ['PROGRAMFILES(X86)'], 'COMODO\Comodo ITSM\cpmlogs')
        prlpath=os.path.join(os.environ['PROGRAMFILES(X86)'], 'COMODO\\Comodo ITSM\\rmmlogs')

    else:
        pmlpath=os.path.join(os.environ['PROGRAMFILES(X86)'], 'COMODO\Comodo ITSM\pmlogs')
        prlpath=os.path.join(os.environ['PROGRAMFILES(X86)'], 'COMODO\\Comodo ITSM\\rmmlogs')
        
else:
    if os.path.exists(os.path.join(os.environ['PROGRAMFILES'], 'COMODO\Comodo ITSM\cpmlogs')):
        pmlpath=os.path.join(os.environ['PROGRAMFILES'], 'COMODO\Comodo ITSM\cpmlogs')
        prlpath=os.path.join(os.environ['PROGRAMFILES'], 'COMODO\\Comodo ITSM\\rmmlogs')

    else:
        pmlpath=os.path.join(os.environ['PROGRAMFILES'], 'COMODO\Comodo ITSM\pmlogs')
        prlpath=os.path.join(os.environ['PROGRAMFILES'], 'COMODO\\Comodo ITSM\\rmmlogs')

file_dic={}
getrmm(prlpath)
key=[]
with open(os.path.join(os.environ['TEMP'], 'report.csv'), 'wb') as c1:
    c1.write('Completed Maintenance Procedures\n')
    c1.write('|Finished Success\n')
    c1.write(' Rmm_Logs :\n')
    for i in e:
        c1.write(i) 
    c1.write('\n\nCompleted Critical and Security Patches Installed\n')
    c1.write('| Pm_Logs :\n')
    tempd=os.path.join(os.environ['temp'], 'templogs.txt')
    tempm=os.path.join(os.environ['temp'], 'tempm.txt')
    templ=os.path.join(os.environ['temp'], 'templ.txt')
    
    logfiles=[os.path.join(pmlpath, i) for i in os.listdir(pmlpath) if i.startswith('PmAgent.log')]
    with open(tempd, 'wb') as w:        
        for i in logfiles:
            with open(i, 'rb') as r:
                 w.write(r.read())
    string=''
    with open(tempd) as r:
        while True:
            line=r.readline()   
            if line:
                if 'Total Installed OS Patches:' in line:
                    string+=line+'||'
                    
            else:
                break

    i=0
    a,b='',''
    ls=string.split('||')
    for i in ls:
        if 'Total' in i:
        
            key=i.split()[1].split(':')[0]
        else:
            pass
        if key[0]==key[1]:
             a,b=key
        break
    if key:
        with open(tempm, 'wb')as w:
            with open(tempd) as r:
                ob=re.search('.*'+a+'.*(\n.*)+.*'+b+'.*', r.read())
                if ob:
                    w.write(ob.group())
    if os.path.exists(tempm) or os.path.exists(templ):
        with open(templ, 'w') as w:
            with open(tempm) as r:
                while True:
                     line=r.readline()
                     if line:
                          if 'Metadata' in line or 'Title:' in line or 'Patch Primary Category: "Security Updates"' in line or 'Patch Primary Category: "Critical Updates"' in line:
                              w.write(line)
                     else:
                          break
    else:
        with open(tempm, 'wb')as f:
            f.write("No information available")
        with open(templ, 'wb')as f:
            f.write("No information available")

    os.remove(tempm)
    lines_seen = set() # holds lines already seen
    out=os.path.join(os.environ['temp'], 'out.txt')
    outfile = open(out, "w")
    for line in open(templ, "r"):
        if line not in lines_seen: # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()

    with open(out) as fr1:
        for i in re.findall('Title:.*\n.*Updates"',fr1.read()):
            ob=re.search('".*\(.*\)"', i)
            if ob:
                t1=ob.group()
                if t1:
                    
                    c1.write('|'+t1[1:-1]+'\n')

    os.remove(templ)
    os.remove(out)

    c1.write('\n\n Softwares Installed\n')
    softw=os.popen('wmic product get name, InstallDate').read()
    softw= re.sub(' +',' ',softw)
    softw=softw.replace('|', '  ')
    c1.write(softw)
    c1.write('\n\nHard Disk Drive Health\n')
    alldrives=[a.strip().split() for a in ecmd('wmic logicaldisk where drivetype=3 get deviceid, freespace, size').split('\n') if len(a.strip().split())==3][1:]
    d={}
    ld=re.findall('Disk\s[0-9]+', ecmd('echo list disk |diskpart'))
    for i in ld:
        f=os.path.join(os.environ['TEMP'], ''.join(i.split())+'.txt')
        with open(f, 'w') as wr:
            wr.write('select %s\nlist volume'%(i))
        lv=re.findall(r'Volume\s[0-9]+\s+[A-Z]', ecmd('diskpart /s '+f))
        os.remove(f)
        templist=[]
        for j in lv:
            vob=re.search('Volume\s[0-9]+\s+', j)
            dl=j.replace(vob.group(), '')+':'
            templist.append(dl)
        d[i]=templist
    dd={}
    for j in d:
        tf=0
        tt=0
        for i in alldrives:
            if i[0] in d[j]:
                tf+=int(i[1])
                tt+=int(i[2])
        dd[j]=[round(float(tt)/(1024*1024*1024), 2), round(float(tf)/(1024*1024*1024), 2), round((float(tt-tf)/tt)*100, 2)]
    for i in dd:
        c1.write('|'+i+'\n||Total Space|'+str(dd[i][0])+' GB'+'\n||Free Space|'+str(dd[i][1])+' GB'+'\n||Disk % Utilized|'+str(dd[i][2])+' %'+'\n\n')





fileToSend=os.path.join(os.environ['TEMP'], 'report.csv')
subject='%s %s Health Report CSV'%(computername(), ipaddress())
if sendmail==1:
    print emailreport(subject,emailto,emailfrom,fileToSend,password,smtpserver,port,msgbody)
else:
    with open(fileToSend) as fr:
        print fr.read().replace('|', '  ')
os.remove(os.path.join(os.environ['TEMP'], 'report.csv'))

