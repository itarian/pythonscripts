import socket
import _winreg
import os
import shutil
import time
import ssl
import time
import ctypes
import urllib2
import getpass
def Avgpres():
    ret=os.popen("wmic product get name").read()
    if 'AVG' in ret:
        AVGUninstall()
    else :
        print "AVG Uninstallation compelted"

def Download2(Download_URL,Download_Path):
    
    fileName = Download_URL.split('/')[-1]
    DownTo = os.path.join(Download_Path, fileName)
    context = ssl._create_unverified_context()
    f=urllib2.urlopen(Download_URL,context=context)
    data=f.read()
    print f.getcode()
    with open(DownTo, "wb") as code:
        code.write(data)
    return DownTo
  

def AVGUninstall():
    Download_Path=os.environ['PROGRAMDATA']
    os.chdir(Download_Path)
    Download_URL ="http://files-download.avg.com/util/tools/AVG_Remover.exe"
    path=Download2(Download_URL,Download_Path)
    out=os.popen(path+' -silent -norestart').read()
    time.sleep(90)
    os.remove(path)
print  "Computer Name: " +socket.gethostname()
print "IP-Address :"
print  socket.gethostbyname(socket.gethostname())
print "\n"

ret=os.popen("wmic product get name").read()
if 'AVG' in ret:
	print "AVG Has installed on endpoint "
	print "Uninstalling  AVG"
	Avgpres()
	AVGUninstall()
	Avgpres()
else :
	print "AVG is not Installed on end point"

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

def Download1(Download_URL,Download_Path):
    print 'Downloading required Comodo Client Security'
    fileName = Download_URL.split('/')[-1]
    DownTo = os.path.join(Download_Path, fileName)
    context = ssl._create_unverified_context()
    f=urllib2.urlopen(Download_URL,context=context)
    data=f.read()
    print f.getcode()
    with open(DownTo, "wb") as code:
        code.write(data)
    print 'Comodo Client security has been downloaded successfully here '+DownTo
    return DownTo


ki=os_platform()
archi=int(filter(str.isdigit, ki))

if archi==64:
	Download_URL ="https://dl.one.comodo.com/download/CIS_x64.msi"
	path="CIS_x64"
elif ki==32:
	Download_URL ="https://dl.one.comodo.com/download/CIS_x86.msi"
	path="CIS_x86"
fileName = Download_URL.split('/')[-1]
Download_Path=os.environ['PROGRAMDATA']
path=Download1(Download_URL,Download_Path)
if archi==64:
    command1='msiexec /i  "'+path+'"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=1 CES_FIREWALL=1 CES_ANTIVIRUS=1  '
elif ki==32:
    command1='msiexec /i  "'+path+'"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=1 CES_FIREWALL=1 CES_ANTIVIRUS=1  '
command=os.popen(command1).read()
time.sleep(90)
os.remove(path)
