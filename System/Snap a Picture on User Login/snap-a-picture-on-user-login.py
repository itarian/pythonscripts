Image_save_path=r"C:\Users\comodo\Desktop\patt" #Give the path where image file should be saved

import os
import zipfile
import ctypes
import sys
import platform
import _winreg
import ssl
import shutil
ssl._create_default_https_context = ssl._create_unverified_context
import subprocess


class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)


pat=os.environ['PROGRAMDATA']
URL=r'https://drive.google.com/uc?export=download&id=1R0XXILwUqi2cz9O3ibYJk72yI-wAXbux'
src_path=os.environ['TEMP']

pat=Image_save_path

def Download(src_path, URL):
    import urllib2
    import os
    fileName = 'webcamimagesave.zip'
    fp = os.path.join(src_path, fileName)
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    if os.path.exists(src_path):
        print " "
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

zip_path=Download(src_path, URL)
file_zip=os.environ['PROGRAMDATA']
file_zip1=file_zip+r'\webcamimagesave'

def filezip(zip_path,file_zip):
    with disable_file_system_redirection():
        with zipfile.ZipFile(zip_path,"r") as zip_ref:
            zip_ref.extractall(file_zip1)
            

filezip(zip_path,file_zip1)

bat=r'''
set mydate=%date:~10,4%_%date:~4,2%_%date:~7,2%_%time:~0,2%%time:~3,2%
%programdata%\webcamimagesave\WebCamImageSave.exe /capture /LabelColor ff0000 /FontBold 1 /FontSize 16/FontName "Arial" /Filename "{}\webcam_logon_image%mydate%.jpg"

'''.format(pat)

path=os.environ['programdata']+"\webcamimagesavee.bat"
with open(path,"w",) as f:
    f.write(bat)


file_to_copy = path
destination_folder = os.environ['programdata']+r"\Microsoft\Windows\Start Menu\Programs\Startup"

import shutil
try:
    shutil.copy2(file_to_copy, destination_folder)
    print "Script is configured to run at each logon and webcam picture will be saved at "+pat
except Exception as err :
    print err

