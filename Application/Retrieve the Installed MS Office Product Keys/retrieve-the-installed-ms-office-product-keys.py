URL=r'https://drive.google.com/uc?export=download&id=1ITCxAqt6sUtxLODohBQsB603YgBPyboc'


import os

src_path=os.environ['TEMP']


import zipfile
import ctypes
import sys
import platform
import _winreg
import ssl
import shutil
import subprocess
from subprocess import PIPE, Popen
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
def check():
    
    with disable_file_system_redirection():
        inst=os.popen("wmic product get name,identifyingnumber").read()
         
        
    return inst


def Download(src_path, URL):
    import urllib2
    import os
    fileName = 'Pro_key.zip'
    fp = os.path.join(src_path, fileName)
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    if not os.path.exists(src_path):
        os.makedirs(src_path)
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    
    return fp


def filezip(zip_path,file_zip):
    with disable_file_system_redirection():
        with zipfile.ZipFile(zip_path,"r") as zip_ref:
            zip_ref.extractall(file_zip1)
            
    return file_zip1

def cmd(pt, tf):
    os.chdir(pt)
    fg='produkey.exe /OfficeKeys 1 /WindowsKeys 0 /IEKeys [0] /SQLKeys [0] /ExchangeKeys [0] /ExtractEdition [0] /stext "%s" /sort "Product Key"'%tf
    obj = subprocess.Popen(fg, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()
    if err:
        print err
    else:
        if os.path.isfile(tf):
                with open(tf, "r+") as df:
                    for i in df:
                        print i
        else:
                print "*****  Error extracting Product key  *****"


inst=check()

if 'Microsoft Office' in inst:
        print "Microsoft Office is installed in the Endpoint\n"
        zip_path=Download(src_path, URL)
        file_zip=os.environ['PROGRAMDATA']
        file_zip1=file_zip+r'\Pro_key'

        if os.path.exists(file_zip1):
            prr=os.listdir(file_zip1)
            for i in prr:
                os.remove(os.path.join(file_zip1,i))
        unz=filezip(zip_path,file_zip1)
        tf=file_zip+'\Office_ProductKey.txt'
        if os.path.isfile(tf):
            os.remove(tf)
            
        cmd(unz, tf)
        try:
                if os.path.exists(file_zip1):
                    prr=os.listdir(file_zip1)
                    for i in prr:
                        os.remove(os.path.join(file_zip1,i))
                os.remove(os.path.join(src_path, "Pro_key.zip"))
        except:
                pass
else:
        print "Microsoft Office is not installed in the Endpoint"


