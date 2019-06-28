URL=r"https://drive.google.com/uc?export=download&id=1f8SheDiyw-DhXW_oql6prxEltpWM6hhB"
import os
from subprocess import PIPE, Popen
import ctypes
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
def Download(URL, DownloadTo = None, FileName = None):
    import urllib
    import ssl
    if FileName:
        FileName = FileName
    else:
        FileName = URL.split('/')[-1]
        
    if DownloadTo:
        DownloadTo = DownloadTo
    else:
        DownloadTo = os.path.join(os.environ['TEMP'])
        
    DF = os.path.join(DownloadTo, FileName)
    with open(os.path.join(DownloadTo, FileName), 'wb') as f:
        try:
            context = ssl._create_unverified_context()
            f.write(urllib.urlopen(URL,context=context).read())
        except:
            f.write(urllib.urlopen(URL).read())
    if os.path.isfile(DF):
        return DF
    else:
        return False
def zip_item(path,final_path):  # Creating ZIP file
    import zipfile
    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extractall(final_path)
    zip_ref.close()
    return final_path

def CMDRUN(Content):
    with disable_file_system_redirection():
        str(Content)
        OBJ = Popen(Content, shell = True, stdout = PIPE, stderr = PIPE)
        out, err = OBJ.communicate()
        print out
        RET = OBJ.returncode
    print RET
    if RET:
        print "Bitdefender Endpoint Security Tools is not Uninstalled "
    else:
        print "Bitdefender Endpoint Security Tools is uninstalled successfully"
        
print "Starting Uninstallation"  
FileName=r"BITDEFENDER_UNINSTALL"
HOMEPATH = os.environ['TEMP']
BDPATH = Download('https://drive.google.com/uc?export=download&id=1f8SheDiyw-DhXW_oql6prxEltpWM6hhB', FileName = 'BITDEFENDER_UNINSTALL.zip')
TEMPHOME = os.path.join(HOMEPATH, 'BITDEFENDER_UNINSTALL')

if os.path.exists(TEMPHOME):
    try:
        shutil.rmtree(TEMPHOME)
    except:
        pass
    
path=zip_item(BDPATH, TEMPHOME)
TEMPHOME = os.path.join(path,'RarSFX1','UninstallTool.exe')
UnInstallBD = '"'+os.path.join(TEMPHOME)+'" /silent /force:Endpoint Security by Bitdefender'
output=CMDRUN(UnInstallBD)
time.sleep(1)
os.chdir(os.environ['TEMP'])
try:
    shutil.rmtree(path)
except:
    pass
try:
    os.remove(BDPATH)
except:
    pass
