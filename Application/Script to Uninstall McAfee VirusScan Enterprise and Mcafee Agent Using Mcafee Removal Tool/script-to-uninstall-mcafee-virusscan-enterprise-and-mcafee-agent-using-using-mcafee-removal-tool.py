
import os
import zipfile
path=os.environ['TEMP']
URL=r'https://drive.google.com/uc?export=download&id=1nMhcB3onFAHtCIg-v8O6jIODhqwICCgv'
fileName = r'MFERemoval100.exe'


def Download(path, URL):
    import urllib2
    import os
    
    fileName = r'MFERemoval100.exe'
    fp = os.path.join(path, fileName)
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    if os.path.exists(path):
        if not os.path.exists(path):
            os.makedirs(path)
        
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    
    
    return fp

src_path=Download(path, URL)
import zipfile
import ctypes
import os
import subprocess
from subprocess import PIPE, Popen
import re
dest_path=os.environ['PROGRAMDATA']
class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
                


os.chdir(os.environ['TEMP'])
command ="MFERemoval100 /noreboot /q /MA /VSE"

 
def check():
        
        obj = subprocess.Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
        result = obj.communicate()[0]
        print "McAfee Uninstalled successfully"
check()
