#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('variableName') with that parameter's name
no=itsm.getParameter('getno')
Head_computer =itsm.getParameter('getcomputer')
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
import os
import subprocess
import shutil,urllib2,time
from subprocess import PIPE, Popen
import socket
import smtplib
import mimetypes
import ctypes
import _winreg
def computername():
    import os
    return os.environ['COMPUTERNAME']
import re,os
import getpass
import socket
import uuid
import math
import string
from ctypes import windll
import time
from math import log

def pretty_size(n,pow=0,b=1024,u='B',pre=['']+[p+'i'for p in'KMGTPEZY']):
    pow,n=min(int(log(max(n*b**pow,1),b)),len(pre)-1),n*b**pow
    return "%%.%if %%s%%s"%abs(pow%(-pow-1))%(n/b**float(pow),pre[pow],u)

mac=(':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])).upper()
from uuid import getnode as get_mac
cmd= os.popen("systeminfo").read()
get=re.findall('Host Name:(.*)',cmd)
Computer_Name=''.join(get).strip().replace(",",'')
symm=re.findall('System Model:(.*)',cmd)
System_Model=''.join(symm).strip().replace(",",'')
ser=re.findall('Product ID:(.*)',cmd)
cmd1=os.popen("wmic bios get serialnumber").read()
Serial_Number=cmd1.split()[1]
list1=[key,Computer_Name,System_Model,Serial_Number] 
d=list1
list_head=['Computer_Name', 'System_Model', 'Serial_Number']

def publish_nonhead():
    import time    
    time.sleep(30)
    from pubnub.pnconfiguration import PNConfiguration
    from pubnub.pubnub import PubNub
    from pubnub.callbacks import SubscribeCallback
    from pubnub.pnconfiguration import PNConfiguration
    from pubnub.pubnub import PubNub
    k1= 'pub-c-e4dca0d8-c948-42e9-a080-3a84922d77c4'
    k2= 'sub-c-ff76b412-17b2-11e8-bb84-266dd58d78d1'
     
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = k2
    pnconfig.publish_key = k1
    pnconfig.ssl = True
     
    pubnub = PubNub(pnconfig)
    import time
    from pubnub.exceptions import PubNubException
    try:
        envelope = pubnub.publish().channel("Channel-n3jbvzcv1").message('%s'%d).sync()
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
    k1= 'pub-c-e4dca0d8-c948-42e9-a080-3a84922d77c4'
    k2= 'sub-c-ff76b412-17b2-11e8-bb84-266dd58d78d1'
     
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
        envelope = pubnub.publish().channel("Channel-n3jbvzcv1").message('%s'%d).sync()
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
        print "Your file is in head computer at "+reportfolder 
	
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
         
        pnconfig.subscribe_key = 'sub-c-ff76b412-17b2-11e8-bb84-266dd58d78d1'
        pnconfig.publish_key = ''

        pubnub = PubNub(pnconfig)
        n=0
        my_listener = SubscribeListener()

        pubnub.subscribe().channels('Channel-n3jbvzcv1').execute()
        fp=os.path.join(os.environ['ProgramData'],"new.csv")
    
        with open(fp,'w') as f:
            for i in range (0,len(list_head)):
                ht=list_head[i]+','
                f.write(ht)
            f.write('\n')
        while True:
            print "Listening..."# endless/long work
            pubnub.add_listener(my_listener)
            result = my_listener.wait_for_message_on('Channel-n3jbvzcv1')
            n=result.message
            pubnub.remove_listener(my_listener)
            k=ast.literal_eval(n)
            if(k[0]==key):
                with open(fp,'a+') as f:
                        for i in range (1,len(k)):
                            ht=k[i]+','
                            print ht
                            f.write(ht)
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

