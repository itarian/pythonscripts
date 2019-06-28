import os
import re
import sys
import getpass
import socket
import time

username=r'abcde' #enter your kaspersky username
password=r'****'  #enter your kaspersky password

print "USER NAME: "+getpass.getuser()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print "IP-ADDRESS :"+(s.getsockname()[0])
from time import gmtime, strftime
time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
temp=os.environ['temp']
def ecmd(CMD, r=False):
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
    from subprocess import PIPE, Popen
    with disable_file_system_redirection():
        OBJ = Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = OBJ.communicate()
    ret=OBJ.returncode
    if r:
        return ret
    else:            
        if ret==0:
            
            return out,ret
        else:
            return err,ret

dm,ret2=ecmd('wmic product get name,identifyingnumber| findstr /i "kaspersky"')
c=0
if ret2!=0:
    print 'Kaspersky products are not installed in your system'
else:
    os.popen('Taskkill /IM avpsus.exe /F').read()
    v=dm.split('\n')
    fin=[]
    for i in range(0,len(v)):
        if len(v[i])!=0:
            fin.append(v[i].split(' ')[0])
    for k in range(0,len(fin)):
        if len(fin[k])!=0:
            
            CMD=('msiexec /x %s KLLOGIN=%s KLPASSWD=%s /qn')%(str(fin[k]),str(username),str(password))
            
            ret3=ecmd(CMD)          
            if ret3[1]==0:
                c=1
                
            else:
                ret1=ecmd('msiexec /x %s /qn'% fin[k])
                if ret1[1]==0:
                    print 'Kaspersky enpoint security is removed from your system'
    if c==1:
        print 'Kaspersky enpoint security is removed from your system'
        print 'kaspersky security center  is removed from your system'
                
          
