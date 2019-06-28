URL_64=['https://download.comodo.com/itsm/windows/cis/update.7z', 'https://download.comodo.com/itsm/windows/cis/x64/cfpconfg.exe', 'https://download.comodo.com/itsm/windows/cis/x64/cmdres.dll', 'https://download.comodo.com/itsm/windows/cis/x64/7za.dll']
URL_32=['https://download.comodo.com/itsm/windows/cis/update.7z', 'https://download.comodo.com/itsm/windows/cis/x32/cfpconfg.exe', 'https://download.comodo.com/itsm/windows/cis/x32/7za.dll', 'https://download.comodo.com/itsm/windows/cis/x32/cmdres.dll']

import os
import ctypes
import re
import time
import shutil

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

def download(path,i):
    import urllib2
    url=i
    usock = urllib2.urlopen(url)                                 
    file_name = url.split('/')[-1]
    fp = os.path.join(path, file_name)
    file_size = int(usock.info().getheaders("Content-Length")[0]) 
    print "Downloading: %s Bytes: %s" % (file_name, file_size)    
    downloaded = 0
    block_size = 8192
    with open(fp, 'wb') as f:
        while True:         
           buff = usock.read(block_size)
           if not buff:                                            
               break
           downloaded = downloaded + len(buff)
           f.write(buff)
    print 'Downloading completed successfully in',fp
    return fp
     

def update(fil,workdir):
    print "Updating CCS to Specified Version\n"
    class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)

    with disable_file_system_redirection():
        os.chdir(workdir)
        CMD='cfpconfg.exe --binaryUpdate --file="'+fil+'"'
        os.popen(CMD)

def execute():
    try:
        workdir=os.environ['PROGRAMDATA']+r'\temp'
        if not os.path.exists(workdir):
            os.mkdir(workdir)      
    except:
        workdir=os.environ['SYTEMDRIVE']       
    URL=[]
    get=[]
    if 'PROGRAMFILES(X86)' in os.environ.keys():
        print "Downloading Required Files...\n"
        URL=URL_64
    else:
        print "Downloading Required Files...\n"
        URL=URL_32        
    for i in URL:
        get.append(download(workdir, i))    
    update(get[0],workdir)
    if os.path.exists("C:\Program Files\COMODO\COMODO Internet Security - Update"):
        print "System is ready to Reboot for Update..."
        os.popen("shutdown -r")
    else:
        print "CCS updation is not found"

    try:
        for i in get:
            os.remove(i)
    except:
        print ' '

with disable_file_system_redirection():
    chk=os.popen('wmic product get name').read()         
    if 'COMODO Client - Security' in chk:
        execute()
    else:
        print 'COMODO Client - Security is not Installed'
