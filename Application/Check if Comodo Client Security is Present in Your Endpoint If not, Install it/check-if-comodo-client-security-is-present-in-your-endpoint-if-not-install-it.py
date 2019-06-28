import os
import re
import time
import sys
import ctypes
import socket
import _winreg
import os
import shutil
import time
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

def Download1(URL, file_path): ### Downloading
    import urllib2
    import os
    print "Download started"
    fileName =URL.split('/')[-1]
    src_path=os.environ['ProgramData']
    fp = os.path.join(src_path, fileName)
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    if os.path.exists(src_path):
        print "Path already exists"
    if not os.path.exists(src_path):
        os.makedirs(src_path)
        print "Path created"
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    print "The file downloaded successfully in specified path"+fp
    return fp

ki=os_platform()
archi=int(filter(str.isdigit, ki))



def check():
        with disable_file_system_redirection():
            inst=os.popen("wmic product get name,identifyingnumber").read()
        return inst

check()
inst=check()
find=re.findall('{.*}\s\sCOMODO\sClient\s-\sSecurity',inst)
if len(find)==0:
    print "\nComodo Client Security is not installed at End point\n"
    if archi==64:
        Download_URL ="https://download.comodo.com/itsm/CIS_x64.msi"    
    elif archi==86:
        Download_URL ="https://download.comodo.com/itsm/CIS_x86.msi"
    fileName = Download_URL.split('/')[-1]
    Download_Path=os.environ['ProgramData']
    fp=os.path.join(Download_Path,fileName)
    path=Download1(Download_URL,Download_Path)
    if archi==64:
        command1='msiexec /i  "'+path+'"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=1 CES_FIREWALL=1 CES_ANTIVIRUS=1  '
        command2='"C:\Program Files (x86)\COMODO\Comodo ITSM\ITSMService.exe" -c 4'
    elif archi==86:
        command1='msiexec /i  "'+path+'"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=1 CES_FIREWALL=1 CES_ANTIVIRUS=1  '
        command2='"C:\Program Files\COMODO\Comodo ITSM\ITSMService.exe" -c 4'
    command=os.popen(command1).read()
    time.sleep(120)
    com=os.popen(command2).read()
    os.remove(fp)
    print 'Comodo Client Security installed Successfully'       
else:
    print "\nComodo Client Security is already installed at End point\n"
