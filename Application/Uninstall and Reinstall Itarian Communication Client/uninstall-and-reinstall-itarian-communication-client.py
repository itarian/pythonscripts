file_name=itsm.getParameter('Enter_the_file_name')#the new token which is downloaded from the portal which you want to reinstall the comodo client communication
import ctypes
import os
import re
import shutil
import subprocess
a=0
URL='https://download.comodo.com/itsm/release/win/communication_client/6.28/itsm_agent.msi'
src_path=os.environ['temp']+"\\"+"comodo"
if not os.path.exists(src_path):
    os.makedirs(src_path)
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
    print file_name+"...Download started"
    fileName = file_name
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
    print file_name+"..Download completed"
    return fp

down_path=Download(src_path, URL)

def check():
    with disable_file_system_redirection():
        inst1=os.popen("wmic product get name,identifyingnumber").read()
    return inst1
inst1=check()
 
if len(inst1)>0:
    find=re.findall('{.*}\s\sITarian\sCommunication\sClient',inst1)
    if len(find)>0:
        final=re.findall('{.*}',find[0])[0]
        if len(final) >0:
            a=1
if a==1:
    BAT=r'''@echo off
wmic product where name="ITarian Communication Client" call uninstall
msiexec /i %s /qn 
'''%(down_path)

    bat_path=os.environ['temp']+"\ComodoInstall.bat"
    with open(bat_path,"w") as f:
        f.write(BAT)
    install=os.popen(bat_path).read()
    print "ITarian Communication Client is uninstalled on Endpoint"
    print "ITarian Communication Client  is installed on Endpoint"
else:
    print "ITarian Communication Client  is not installed on Endpoint"
def remove():
    try:
        shutil.rmtree(src_path)
        os.remove(bat_path)
    except:
        pass
remove()
