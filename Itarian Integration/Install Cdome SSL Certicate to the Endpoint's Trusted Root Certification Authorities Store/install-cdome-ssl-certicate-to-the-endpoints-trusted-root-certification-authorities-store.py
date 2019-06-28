Download_URL ="https://s3.amazonaws.com/domeshieldcert/blockpage.pem"

import os
import zipfile
import urllib
import urllib2
import ssl
import urllib
import time
import ctypes

fileName = Download_URL.split('/')[-1]
Download_Path=os.environ['PROGRAMDATA']
Identify_Os = "wmic os get Caption"
Ent_Cmd =  'certutil.exe /addstore /enterprise /f  "Root" "%s"'%(os.path.join(Download_Path, fileName))
Other_Cmd = 'certutil.exe /addstore /f  "Root"  "%s"'%(os.path.join(Download_Path, fileName))


class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

            
def Download(Download_URL,Download_Path):
    print 'Downloading required certificate'
    fileName = Download_URL.split('/')[-1]
    DownTo = os.path.join(Download_Path, fileName)
    context = ssl._create_unverified_context()
    f=urllib2.urlopen(Download_URL,context=context)
    data=f.read()
    print f.getcode()
    with open(DownTo, "wb") as code:
        code.write(data)
    print 'The required certificate has been downloaded successfully here '+DownTo

Download(Download_URL,Download_Path)
with disable_file_system_redirection():        
    os_details = os.popen(Identify_Os).read()
    print os_details

if "Enterprise" and "7" in os_details:
    os.chdir(Download_Path)
    with disable_file_system_redirection():
        print 'Installing certificate begins....'        
        add_ent_cert = os.popen(Ent_Cmd).read()
        print 'Certificate installed sucessfully'
        print add_ent_cert
else:
    os.chdir(Download_Path)
    with disable_file_system_redirection():
        print 'Installing certificate begins....'
        add_other_cert = os.popen(Other_Cmd).read()
        print 'Certificate installed sucessfully'
        print add_other_cert

os.chdir(Download_Path)
os.remove(fileName)
