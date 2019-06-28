no=50        #Edit the xx parameter as Device Timeout. Eg if you have 500 enrolled endpoints then that xx must "100".
Head_computer=r'XXXXXXX' # Head computer to send the email 
emailto='XXX@mail.com' # Email address to send the report 
Head_computer=Head_computer.upper()
KI=list(Head_computer)
KI.insert(0,str(no))
import datetime
KI.insert(len(KI),datetime.datetime.now().strftime("%Y%m%d"))
key="".join(KI)

import ast
import threading
import time
import os
from subprocess import PIPE, Popen
import ctypes
import shutil
import zlib, base64
def Email(fileToSend,To):
    from mailjet_rest import Client
    import os
    api_key='3e70858a7a5c5fbc245a662d5d9aa238'   # API KEY of Mail Jet 
    api_secret= 'a337abcc84d8fb062f6f1597d966ae6f'  # API SECRET KEY of Mail Jet
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    import base64
    with open(fileToSend, 'rb') as fp:
        ki=base64.b64encode(fp.read())
    data = {
      'Messages': [
                    {
                            "From": {
                                    "Email": "c1operations123@gmail.com",
                            },
                            "To": [
                                    {
                                            "Email": "%s"%To,
                                    }
                            ],
                            "Subject": "HEALTH REPORT ",
                            "TextPart": "Dear passenger 1, welcome to Mailjet! May the delivery force be with you!",
                            "HTMLPart": """<h3> Hi

        Please find the attachment which contains all the device reports 

        Thank you.</h3>""",
                            "Attachments": [
                                    {
                                            "ContentType": "text/csv",
                                            "Filename": "Finalreport.csv",
                                            "Base64Content": "%s"%ki
                                    }
                            ]
                    }
            ]
    }
    result = mailjet.send.create(data=data)
    ret=result.status_code
    if ret==200:
        out=result.json()
        out=str(out)
        if "success" in out:
            print "Email Sent Successfully"
    else:
        print "Error sending email"
def Download(URL, DownloadTo = None, FileName = None):
    import urllib
    import ssl
    if FileName:
        FileName = FileName
    else:
        FileName = URL.split('/')[-1]
        
    if DownloadTo:
        DownloadTo = DownloadTo
    else:
        DownloadTo = os.path.join(os.environ['TEMP'])
        
    DF = os.path.join(DownloadTo, FileName)
    with open(os.path.join(DownloadTo, FileName), 'wb') as f:
        try:
            context = ssl._create_unverified_context()
            f.write(urllib.urlopen(URL,context=context).read())
        except:
            f.write(urllib.urlopen(URL).read())
    if os.path.isfile(DF):
        return DF
    else:
        return False
def zip_item(path,final_path):  # Creating ZIP file
    import zipfile
    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extractall(final_path)
    zip_ref.close()
    return final_path
def Import_pubnub(DEST):
    BDPATH = Download(r'https://drive.google.com/uc?export=download&id=1R1KFmrC0jh6TOdCFePt2SNTbu_ti_CpP', FileName = 'PUBNUB.zip')
    SRC = os.path.join(os.environ['TEMP'])
    path=zip_item(BDPATH,SRC)
    SRC = os.path.join(os.environ['TEMP'],'PUBNUB')
    from distutils.dir_util import copy_tree
    copy_tree(SRC, DEST)
    import pubnub 
    from pubnub.pnconfiguration import PNConfiguration
    from pubnub.pubnub import PubNub
    from pubnub.callbacks import SubscribeCallback
    print "Pubnub is imported"

    
    return DEST

def ipaddress():
    import socket
    return socket.gethostbyname(socket.gethostname())    
def computername():
    import os
    return os.environ['COMPUTERNAME']
import os
import re
import getpass
import socket
import uuid
import math
import string
from ctypes import windll
import time
import zlib
from math import log
import random
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
e=[]
b=[]
d="Rmm_dll"
import _winreg

import os
def ipaddress():
    import socket
    return socket.gethostbyname(socket.gethostname())    
def computername():
    import os
    return os.environ['COMPUTERNAME']


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
    jo=''.join(e)
    return jo


    
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
key1=[]
with open(os.path.join(os.environ['TEMP'], 'report.csv'), 'wb') as c1:
    name=os.popen("hostname").read()
    print name
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
            key1=i.split()[1].split(':')[0]
             
        else:
            pass
    
    
        if key1==key[0]:
        	a,b=key1
            
        break
    
    if key1:
        
        with open(tempm, 'wb')as w:
            with open(tempd) as r:
                ob=re.search('.*'+a+'.*(\n.*)+.*'+b+'.*', r.read())
                
                if ob:
                    w.write(ob.group())
##        else:
##            with open(tempm, 'wb')as f:
##                f.write("No information available")
            
##    os.remove(tempd)
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

##    os.remove(templ)
##    os.remove(out)
    c1.write('\n\n Softwares Installed\n')
    softw=os.popen('wmic product get name, InstallDate ,Description ,InstallState').read()
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

with open(fileToSend) as fr:
    ki=fr.read().replace(' ','|')



con=computername()
ip=ipaddress()
result=[]
result.append(key+'COMPUTERNAME:'+','+con+'\n')
result.append('IPADDRESS:'+','+ip+'\n')
result.append(str(ki))
result.append('\n')

    
d=result
d=''.join(d)
code =  base64.b64encode(zlib.compress(d,9))
try:
    os.remove(pm1)
    os.remove(pm2)
    os.remove(pm3)
except:
    pass
print "Successfully collected OS Patch logs"

def publish_nonhead():
    import time    
    time.sleep(30)
    from pubnub.pnconfiguration import PNConfiguration
    from pubnub.pubnub import PubNub
    from pubnub.callbacks import SubscribeCallback
    from pubnub.pnconfiguration import PNConfiguration
    from pubnub.pubnub import PubNub
    k1= 'pub-c-529ac86d-f8bc-4094-9196-1fe0652ebc4f'
    k2= 'sub-c-5dec13b4-1c6f-11e8-9e0d-86843e43dc8b'
     
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = k2
    pnconfig.publish_key = k1
    pnconfig.ssl = True
     
    pubnub = PubNub(pnconfig)
    import time
    from pubnub.exceptions import PubNubException
    try:
        envelope = pubnub.publish().channel("Channel-82ldwdilv").message(code).sync()
        print("publish timetoken: %d" % envelope.result.timetoken)
    except PubNubException as e:
            print e

def publish(no):
    import pubnub 
    from pubnub.pnconfiguration import PNConfiguration
    from pubnub.pubnub import PubNub
    from pubnub.callbacks import SubscribeCallback

    from pubnub.pnconfiguration import PNConfiguration
    from pubnub.pubnub import PubNub
    k1= 'pub-c-529ac86d-f8bc-4094-9196-1fe0652ebc4f'
    k2= 'sub-c-5dec13b4-1c6f-11e8-9e0d-86843e43dc8b'
     
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = k2
    pnconfig.publish_key = k1
    pnconfig.ssl = True
     
    pubnub = PubNub(pnconfig)
    import time
    s=3*no
    print s
    time.sleep(s)
    


    from pubnub.exceptions import PubNubException
    try:
        envelope = pubnub.publish().channel("Channel-82ldwdilv").message(code).sync()
        print("publish timetoken: %d" % envelope.result.timetoken)
        
        app_process=os.getpid()
        app_process=str(app_process)
        import subprocess;
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

        time.sleep(5)
        reportfolder=os.path.join(os.environ['ProgramData'],"new.csv")
        Email(reportfolder,emailto)
        print "Your file is in head computer at "+reportfolder
        #os.remove(reportfolder)
        
        with disable_file_system_redirection():
            process=subprocess.Popen(['taskkill', '/F','/PID',app_process],shell=True,stdout=subprocess.PIPE);
            result=process.communicate()[0]
            print (result)
    except PubNubException as e:
            print e


class LongFunctionInside(object):
    lock_state = threading.Lock()
    working = False

    def long_function(self, timeout,no):

        self.working = True

        timeout_work = threading.Thread(name="thread_name", target=self.work_time, args=(timeout,))
        timeout_work.setDaemon(True)
        timeout_work.start()
        import logging

        import pubnub
        from pubnub.exceptions import PubNubException
        from pubnub.pnconfiguration import PNConfiguration
        from pubnub.pubnub import PubNub, SubscribeListener

        import time
        import os
        pnconfig = PNConfiguration()
         
        pnconfig.subscribe_key = 'sub-c-5dec13b4-1c6f-11e8-9e0d-86843e43dc8b'
        pnconfig.publish_key = ''

        pubnub = PubNub(pnconfig)
        n=0
        my_listener = SubscribeListener()

        pubnub.subscribe().channels('Channel-82ldwdilv').execute()
        fp=os.path.join(os.environ['ProgramData'],"new.csv")
        with open(fp,'w+') as f:
                f.write("\t\t\t\t HEALTH REPORT\t\t\t\t")
                f.write('\n\n\n\n\n')
        import sys
        reload(sys)
        sys.setdefaultencoding('utf8')
        while True:
            print "Listening..."# endless/long work
            pubnub.add_listener(my_listener)
            result = my_listener.wait_for_message_on('Channel-82ldwdilv')
            data=result.message
            
            pubnub.remove_listener(my_listener)
            k=[]
            uno= zlib.decompress(base64.b64decode(data))
            #print uno
            a=len(key)
            f=''
            for i in range (0,a):
                f+=uno[i]
            print f
            if (f==key):
                print "hai"
                with open(fp,'a+') as f:
                    print "writing fin file"
                    f.write(uno[a:])
                    f.write(",\n\n")

                
            if not self.working:  # if state is working == true still working
                break
        self.set_state(True)

    def work_time(self, sleep_time):
        print sleep_time# thread function that just sleeping specified time,
        
        time.sleep(sleep_time)
        if self.working:
            publish(no)            
            self.set_state(False)

    def set_state(self, state):  # secured state change
        while True:
            self.lock_state.acquire()
            try:
                self.working = state
                break
            finally:
                self.lock_state.release()

HOMEPATH = r"C:\Program Files (x86)"
if os.path.exists(HOMEPATH):
        HOMEPATH = r"C:\Program Files (x86)"
else:
    HOMEPATH =r"C:\Program Files"

DEST= os.path.join(HOMEPATH,r'COMODO\Comodo ITSM\Lib\site-packages')
Folders=os.listdir(DEST)
Nodow=0
Del_folders=['certifi', 'certifi-2018.1.18.dist-info','chardet', 'chardet-3.0.4.dist-info', 'Cryptodome', 'pubnub', 'pubnub-4.0.13.dist-info', 'pycryptodomex-3.4.12.dist-info','requests']
for i in Del_folders:
    if i in Folders:
        Nodow=Nodow+1
if Nodow>7:
    c=0
else:
    DEST=Import_pubnub(DEST)
computer=os.environ['computername']
if computer==Head_computer :
    lw = LongFunctionInside()
    lw.long_function(0.1,no)
else:
    print "publish"
    publish_nonhead()
