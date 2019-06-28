find=['xx','yy']               #Given the specific software you need to find on your devices  Eg.['comodo client - communication','Google Chrome','Mozilla Thunderbird']
no=xx      #Edit the xx parameter as Device Timeout. Eg if you have 500 enrolled endpoints then that xx must "100".
Head_computer=r'change me' # Head computer to send the email 
emailto='xxx@yyy.com' # Email address to send the report 
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
                            "Subject": "3RD PARTY APPLICATION PATCH INVENTORY REPORT OF ALL ",
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
## detect all installed software through registry key            
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
                    _winreg.CloseKey(oK1)
                    ln.append(DN)
                except:
                    pass
                i += 1
            except:
                break
        _winreg.CloseKey(oK)
        return ln
    except:
        return ln

## detect whether the computer is 32 bit or 64 bit
import _winreg
import os
rK = _winreg.HKEY_LOCAL_MACHINE
sK = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
openedKey = _winreg.OpenKey(rK, sK, 0, _winreg.KEY_READ)
arch, bla = _winreg.QueryValueEx(openedKey, 'PROCESSOR_ARCHITECTURE')
arch = str(arch)
_winreg.CloseKey(openedKey)
## sorting all collected data from all the way, filtered duplicates and listed the final result!
if arch == 'AMD64':
    fList = DNDS(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_32KEY | _winreg.KEY_READ)
    fList.extend(DNDS(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_64KEY | _winreg.KEY_READ))
    fList.extend(DNDS(_winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_32KEY | _winreg.KEY_READ))
    fList.extend(DNDS(_winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_64KEY | _winreg.KEY_READ))
else:
    fList = DNDS(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_READ)
    fList.extend(DNDS(_winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_READ))
fList = set(fList)
final=sorted(fList)
        
fnl_list=[]
fnl_nf=[]
for i in final:
    if  i.lower() in [x.lower() for x in find]:
            fnl_list.append(i)
fnl_nf.append(key)
fnl_nf.append(computername())
fnl_nf.append(ipaddress())
for i in find:
    if i.lower() not in [x.lower() for x in fnl_list]:
        fnl_nf.append(i+" - Not Found")
    if i.lower() in [x.lower() for x in fnl_list]:
        fnl_nf.append(i+" - Found")
d= fnl_nf
print d



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
        envelope = pubnub.publish().channel("Channel-82ldwdilv").message(d).sync()
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
        envelope = pubnub.publish().channel("Channel-82ldwdilv").message(d).sync()
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
        os.remove(reportfolder)
        
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
        header=[]
        header.append('COMPUTER NAME')
        header.append('IP ADDRESS')
        for i in range(0,len(fnl_nf)-3):
            header.append('APPLICATION '+str(i+1))
        with open(fp,'w+') as f:
            f.write("\t\t\t\tFIND THE SPECIFIC APPLICATION REPORT FOR ALL DEVICES\t\t\t\t\n")
            for i in range(0,len(header)):
                f.write(str(header[i])+',')
            f.write('\n')
            import sys
            reload(sys)
            sys.setdefaultencoding('utf8')
            
        while True:
            print "Listening..."# endless/long work
            pubnub.add_listener(my_listener)
            result = my_listener.wait_for_message_on('Channel-82ldwdilv')
            n=result.message
            pubnub.remove_listener(my_listener)
            
            if(n[0]==key):
                with open(fp,'a') as f:
                    for i in range(1,len(n)):
                        f.write(n[i]+',')
                    f.write('\n')


                
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
    publish_nonhead()
