Folder_Path=r"C:\Users"   #Provide your path to folder
import os
import platform
import ssl
import subprocess
from subprocess import PIPE, Popen
import time
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

def Download(src_path, URL,fp):
    import urllib2
    
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    try:
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        parsed = urllib2.urlopen(request,context=gcontext)
    except:
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

def os_platform():
    true_platform = os.environ['PROCESSOR_ARCHITECTURE']
    try:
            true_platform = os.environ["PROCESSOR_ARCHITEW6432"]
    except KeyError:
            pass
            #true_platform not assigned to if this does not exist
    return true_platform

Folder=os.environ['programdata']+r"\Noproblem"
if not os.path.exists(Folder):
    os.mkdir(Folder)
fileName=r"accesschk.exe"
src_path=Folder
fp = os.path.join(src_path, fileName)    
ki=os_platform()
archi=int(filter(str.isdigit, ki))
URL64=r"https://docs.google.com/uc?export=download&id=1AbFwLFaidzWc5do4SP-wmAIbFXgFt6Ob"
URL32=r"https://docs.google.com/uc?export=download&id=1nPO--kIM_oRzdKiIfWsUwJijRspxjMBk"
if archi==64:
    Excutable_path=Download(Folder, URL64,fp)
else:
    Excutable_path=Download(Folder, URL32,fp)   
output=Folder+"\\"+"accesschk.exe -accepteula -d "+Folder_Path
with disable_file_system_redirection():
    obj = subprocess.Popen(output, shell = True, stdout = PIPE, stderr = PIPE)
    result = obj.communicate()[0]
    print result
    try:
        shutil.rmtree(Folder)
    except:
        pass


