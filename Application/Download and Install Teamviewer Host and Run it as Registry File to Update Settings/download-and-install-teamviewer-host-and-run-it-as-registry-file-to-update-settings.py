Download_URL ="https://dl.tvcdn.de/download/TeamViewer_Host_Setup.exe"   #Provide the download URL
#Provide the content of .reg file here
content ='''Windows Registry Editor Version 5.00                         

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TeamViewer]
"Start"=dword:0x000000002
'''

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
import subprocess
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


def Download1(Download_URL, Download_Path): ### Downloading
    import urllib2
    import os
    print "Download started"
    fileName =Download_URL.split('/')[-1]
    src_path=os.environ['ProgramData']
    fp = os.path.join(src_path, fileName)
    request = urllib2.Request(Download_URL, headers={'User-Agent' : "Magic Browser"})
    ssl._create_default_https_context = ssl._create_unverified_context
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


command=r'/S /SUPPRESSMSGBOXES'
fileName = Download_URL.split('/')[-1]
Download_Path=os.environ['ProgramData']
fp=os.path.join(Download_Path,fileName)
path=Download1(Download_URL,Download_Path)
process=subprocess.Popen([path, command],stdout=subprocess.PIPE);
result=process.communicate()[0]
time.sleep(90)
os.remove(fp)
print 'TeamViewer installed Successfully'

update=os.environ['ProgramData']
update1=update+'\\'+'registry.reg'
with open(update1,'w') as w:
    w.write(content +"\n")
    print"file written successfully in : "+update1

os.chdir(update)
c=os.popen("regedit /s registry.reg").read();
print c
print "TeamViewer host .reg file is runned successfully"

