no=xx   #Edit the xx parameter as Device Timeout. Eg if you have 500 enrolled endpoints then that xx must "100".
Head_computer=r'CHANGE_ME' # Head computer to send the email 
emailto=r'CHANGE_ME' # Email address to send the report 
Head_computer=Head_computer.upper()
KI=list(Head_computer)
KI.insert(0,str(no))
import datetime
KI.insert(len(KI),datetime.datetime.now().strftime("%Y%m%d"))
KEY="".join(KI)
import ast
import threading
import time
import os
from subprocess import PIPE, Popen
import ctypes
import shutil
import socket,re
import sys
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
                            "Subject": "Disk Usage Percentage of all devices ",
                            "TextPart": "Dear passenger 1, welcome to Mailjet! May the delivery force be with you!",
                            "HTMLPart": """<h3> Hi \n

        Please find the attachment which contains all the device reports \n

        Thank you.</h3>""",
                            "Attachments": [
                                    {
                                            "ContentType": "text/csv",
                                            "Filename": "Diskreport.csv",
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
def computername():
    return os.environ['COMPUTERNAME']
def ipaddress():
    return socket.gethostbyname(socket.gethostname())
vbs=r'''
Sub DpySpaceInfo(ByVal infotype, ByVal drvSpace, ByVal percentage) 
 
    textline = Space(12 - Len(infotype)) & infotype & Space(17 - Len(drvSpace)) & drvSpace 
    'If percentage <> "" Then textline = textline & Space(33 - Len(textline)) & percentage 
    If percentage <> "" Then textline = textline & Space(11 - Len(percentage)) & percentage 
    WScript.Echo textline 
 
End Sub 
 
' Function to calculate the used and free space on the disk drive. 
Sub GetDriveSpace(ByRef drive) 
 
    totalSpace = drive.TotalSize / 1024 
    freeSpace = drive.AvailableSpace / 1024 
    percentFree = freeSpace / totalSpace 
    percentUsed = 1 - percentFree 
     
    dpyUsedSpace = FormatNumber(totalSpace - freeSpace, 0, vbTrue, vbFalse, vbTrue) & " KB" 
    dpyFreeSpace = FormatNumber(freeSpace, 0, vbTrue, vbFalse, vbTrue) & " KB" 
    dpyTotalSpace = FormatNumber(totalSpace, 0, vbTrue, vbFalse, vbTrue) & " KB" 
    dpyPercentUsed = FormatPercent(percentUsed, 2, vbTrue, vbFalse, vbTrue) 
    dpyPercentFree = FormatPercent(percentFree, 2, vbTrue, vbFalse, vbTrue)
    WScript.Echo "DRIVE " & drive.DriveLetter & ":" &dpyPercentFree

     
End Sub 
 
Set oFileSystem = CreateObject("Scripting.FileSystemObject") 
Set drivesList = oFileSystem.Drives 
 
' Iterage through all drives ignoring all but fixed drives. 
For Each d In drivesList 
    If d.DriveType = 2 Then GetDriveSpace d 
Next
'''
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


def runvbs(vbs):
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.isdir(workdir): 
        os.mkdir(workdir)
    with open(workdir+r'\temprun.vbs',"w") as f :
        f.write(vbs)        
    with disable_file_system_redirection():
        Percentage=os.popen('cscript.exe "'+workdir+r'\temprun.vbs"').read()
        
    if os.path.isfile(workdir+r'\temprun.vbs'):
        os.remove(workdir+r'\temprun.vbs')
    return Percentage



def Drive(KEY):
    SAM=[]
    per=[]
    percent=runvbs(vbs)
    SAM.append(KEY)
    SAM.append(computername())
    SAM.append(ipaddress())
    freepercent=re.findall('DRIVE (.*)',percent)
    for val in freepercent:
        val1=re.sub(r":(.*)", "", val)
        val=re.sub(r"(.*):", "", val)
        val=re.sub(r"%", "", val)
        val=float(val)
        freepercentage=100-val
        per.append(str(freepercentage))
    drive=os.popen('wmic logicaldisk WHERE DriveType=3 get name').read()
    list_of_drives=drive.split()[1:]
    def disk_usage(path):
        _, total, free = ctypes.c_ulonglong(), ctypes.c_ulonglong(), \
                           ctypes.c_ulonglong()
        if sys.version_info >= (3,) or isinstance(path, unicode):
            fun = ctypes.windll.kernel32.GetDiskFreeSpaceExW
        else:
            fun = ctypes.windll.kernel32.GetDiskFreeSpaceExA
        ret = fun(path, ctypes.byref(_), ctypes.byref(total), ctypes.byref(free))
        if ret == 0:
            raise ctypes.WinError()
        used = total.value - free.value
        return [total.value, used, free.value]

    def bytes2human(n):
        symbols = ('KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i+1)*10 
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.1f%s' % (value, s)
        return n

    k=[disk_usage(i) for i in list_of_drives]
    fnl=[]
    for i in k:
        for j in i:
                SAM.append(bytes2human(j))
    j=3
    for i in list_of_drives:
        SAM.insert(j,i)
        j=j+4
    j=7
    for i in per:
        SAM.insert(j,i)
        j=j+5
    print SAM
    if len(SAM)>=8:
        j=8
        for i in per:
            SAM.insert(j,"\n"+",")
            j=j+6
    else:
        j=8
        SAM.insert(j,"\n")
            
        
    return SAM


list_head=['Computer_Name', 'IP_Address',"Drive_name","Total_Space","Used_Space","Free_Space","Percentage_of_usage"]
def publish_nonhead():
    import time    
    time.sleep(30)
    from pubnub.pnconfiguration import PNConfiguration
    from pubnub.pubnub import PubNub
    from pubnub.callbacks import SubscribeCallback
    from pubnub.pnconfiguration import PNConfiguration
    from pubnub.pubnub import PubNub
    publish_key1= 'pub-c-7a797a24-388e-411c-b848-9bd170919784'
    subscribe_key1= 'sub-c-b1b31f80-179a-11e8-95aa-1eb18890f15d'
     
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = subscribe_key1
    pnconfig.publish_key = publish_key1
    pnconfig.ssl = True
     
    pubnub = PubNub(pnconfig)
    import time
    from pubnub.exceptions import PubNubException
    try:
		
        envelope = pubnub.publish().channel("Channel-706fxzjkv").message(Drive(KEY)).sync()
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
    publish_key1= 'pub-c-7a797a24-388e-411c-b848-9bd170919784'
    subscribe_key1= 'sub-c-b1b31f80-179a-11e8-95aa-1eb18890f15d'
     
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = subscribe_key1
    pnconfig.publish_key = publish_key1
    pnconfig.ssl = True
     
    pubnub = PubNub(pnconfig)
    import time
    s=3*no
    time.sleep(s)  


    from pubnub.exceptions import PubNubException
    try:
        envelope = pubnub.publish().channel("Channel-706fxzjkv").message(Drive(KEY)).sync()
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
         
        pnconfig.subscribe_key = 'sub-c-b1b31f80-179a-11e8-95aa-1eb18890f15d'
        pnconfig.publish_key = ''

        pubnub = PubNub(pnconfig)
        n=0
        my_listener = SubscribeListener()

        pubnub.subscribe().channels('Channel-706fxzjkv').execute()
        fp=os.path.join(os.environ['ProgramData'],"new.csv")
        sample=''
        for i in list_head:
            if i == None:
                sample=sample+"None"+","
            else:
                sample=sample+i+","
        with open(fp,'w') as f:
            f.write(sample)
            f.write('\n')
        while True:
            print "Listening..."# endless/long work
            pubnub.add_listener(my_listener)
            result = my_listener.wait_for_message_on('Channel-706fxzjkv')
            pubnub.remove_listener(my_listener)
            result=result.message
            print result[0]
            sample=""
            if(result[0]==KEY):
                with open(fp,'a+') as f:
                    for i in range(1,len(result)):
                        if result[i] == None:
                            sample=sample+"None"+","
                        else:
                            sample=sample+result[i]+","
                    f.write(sample)                   
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
fp=os.path.join(os.environ['ProgramData'],"new.csv")
if os.path.exists(fp):
	try:
		os.remove(fp)
	except:
		pass

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
import os
if computer==Head_computer :
    lw = LongFunctionInside()
    lw.long_function(0.1,no)
else:
    publish_nonhead()
