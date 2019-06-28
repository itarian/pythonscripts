import os
URL=r'https://www.mediafire.com/file/2d3bk2zqa7gjb96/DesktopInfo.zip'
src_path=os.environ['TEMP']
print src_path

import zipfile
import ctypes
import sys
import platform
import _winreg
import ssl
import shutil
ssl._create_default_https_context = ssl._create_unverified_context


class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)

def Download(src_path, URL):
    import urllib2
    import os
    print "Download started"
    fileName = 'Desktop_info.zip'
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
    print "The file downloaded successfully in specified path"
    return fp

zip_path=Download(src_path, URL)
print zip_path
file_zip=os.environ['PROGRAMDATA']
file_zip1=file_zip+r'\info'

def filezip(zip_path,file_zip):
    with disable_file_system_redirection():
        with zipfile.ZipFile(zip_path,"r") as zip_ref:
            zip_ref.extractall(file_zip1)
            print 'file unzipped to ' +file_zip1

filezip(zip_path,file_zip1)

if 'PROGRAMW6432' in os.environ.keys():
    path=r'C:\Program Files (x86)\DesktopInfo'
    shutil.copytree(file_zip1,path)
    file_to_startup = r'C:\Program Files (x86)\DesktopInfo\DesktopInfo.exe'
    
else:
    path=r'C:\Program Files\DesktopInfo'
    shutil.copytree(file_zip1,path)
    file_to_startup = r'C:\Program Files\DesktopInfo\DesktopInfo.exe'

    
handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"Software\Microsoft\Windows\CurrentVersion\Run", 0, _winreg.KEY_ALL_ACCESS)
_winreg.SetValueEx(handle, "DesktopInfo", 0, _winreg.REG_SZ, file_to_startup)
print "Adding the file into Registry for Autostart...."
print 'Restart the endpoint to apply changes ....'
shutil.rmtree(file_zip1)

