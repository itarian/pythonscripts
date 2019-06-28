import os
import ctypes
import re
import time
import socket
import _winreg
import shutil
import ssl
import urllib2
import getpass

def os_platform():
    true_platform = os.environ['PROCESSOR_ARCHITECTURE']
    try:
            true_platform = os.environ["PROCESSOR_ARCHITEW6432"]
    except KeyError:
            pass
            #true_platform not assigned to if this does not exist
    return true_platform

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
def check():
    
    with disable_file_system_redirection():
        inst=os.popen("wmic product get name,identifyingnumber").read()
    return inst
        
def check1():
    with disable_file_system_redirection():
        inst1=os.popen("wmic product get name,identifyingnumber").read()
    return inst1
    
def install_CCS():
    def Download1(Download_URL,Download_Path):
        print 'Downloading required Comodo Client Security'
        fileName = Download_URL.split('/')[-1]
        DownTo = os.path.join(Download_Path, fileName)
        try:
            context = ssl._create_unverified_context()
            f=urllib2.urlopen(Download_URL,context=context)
        except:
            f=urllib2.urlopen(Download_URL)
        data=f.read()
        print f.getcode()
        with open(DownTo, "wb") as code:
            code.write(data)
        print 'Comodo Client security has been downloaded successfully here '+DownTo
        print 'Installing Comodo Client Security'
        return DownTo
    if archi==64:
        Download_URL ="https://download.comodo.com/itsm/CIS_x64.msi"
        path="CIS_x64"
    elif archi==86:
        Download_URL ="https://download.comodo.com/itsm/CIS_x86.msi"
        path="CIS_x86"
    fileName = Download_URL.split('/')[-1]
    Download_Path=os.environ['PROGRAMDATA']
    path=Download1(Download_URL,Download_Path)
    if archi==64:
        command1='msiexec /i  "'+path+'"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=1 CES_FIREWALL=1 CES_ANTIVIRUS=1  '
    elif archi==86:
        command1='msiexec /i  "'+path+'"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=1 CES_FIREWALL=1 CES_ANTIVIRUS=1  '
    command=os.popen(command1).read()
    time.sleep(90)
    os.remove(path)
    print 'Comodo Client Security installed Successfully\n'


def Uninstall_SEP():
    k=[];
    with disable_file_system_redirection():
        guid=os.popen('powershell.exe "get-wmiobject Win32_Product | Format-Table Name,IdentifyingNumber" |  findstr /i /c:"Symantec"  | sort').read();
        print(guid)

    k.append(re.findall("{.*",guid));
    j=[];
    for i in k[0]: j.append(i);
    print j;

    with disable_file_system_redirection():
        for i in j: 
            out=os.popen('msiexec.exe /x '+i+' /quiet REBOOT=ReallySuppress REMOVE=ALL').read();
            print(out);
            time.sleep(10);
            print "Symantec Endpoint protection is Uninstalled Successfully from the Endpoint"


    
ki=os_platform()
archi=int(filter(str.isdigit, ki))

inst=check()
inst1=check1()

find1=re.findall('{.*}\s\sSymantec',inst1)
if len(find1)==0:
    print "Symantec Endpoint protection is not installed at End point\n"

else:
    print "Symantec Endpoint protection is installed at End point\n"
    Uninstall_SEP()

find=re.findall('{.*}\s\sCOMODO\sClient\s-\sSecurity',inst)
if len(find)==0:
    print "\nComodo Client Security is not installed at End point\n"
    install_CCS()
else:
    print "\nComodo Client Security is already installed at End point\n"



