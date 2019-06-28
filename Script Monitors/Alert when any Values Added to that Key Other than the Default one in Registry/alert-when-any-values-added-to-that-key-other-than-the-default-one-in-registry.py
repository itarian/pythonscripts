reg_path=r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Microsoft Antimalware\Exclusions\Paths'#edit with your registry path here
import os
import ctypes
import socket
import difflib
import re
import sys
import platform

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

def os_platform():
    true_platform = os.environ['PROCESSOR_ARCHITECTURE']
    try:
            true_platform = os.environ["PROCESSOR_ARCHITEW6432"]
    except KeyError:
            pass
            #true_platform not assigned to if this does not exist
    return true_platform

name=os.environ['username']
print 'PC-NAME : '+name
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print "IP-ADDRESS : " + (s.getsockname()[0])
fileToSend1=os.path.join(os.environ['ProgramData'],'registry.txt')
fileToSend2=os.path.join(os.environ['ProgramData'],'new_registry.txt')


ki=os_platform()
archi=int(filter(str.isdigit, ki))


def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))

def write(c):
    fn="registry.txt"    
    fn1='new_registry.txt'
    if os.path.exists(fileToSend1):
        with open(fileToSend2, 'w+') as f:
                f.write(c)
               
    else:
        with open(fileToSend1, 'w+') as f:
                f.write(c)
                
    if not os.path.exists(fileToSend2):
        with open(fileToSend1, 'w+') as f:
                f.write(c)
        with open(fileToSend2, 'w+') as f1:
                f1.write(c)
            

def compare():
    file1=fileToSend1
    file2=fileToSend2
    c=0
    f=open(file1,'r')  
    f1=open(file2,'r') 
    str1=f.read()
    str2=f1.read()
    str1=str1.split() 
    str2=str2.split()
    d=difflib.Differ()     
    diff=list(d.compare(str2,str1))
    diff1="\n".join(diff)
    diff2=re.findall("- (.*)",diff1)
    diff3=re.findall("\+ (.*)",diff1)
    if diff2:
        c=1
    if diff3:
        c=1
    return c

import _winreg 
key = reg_path
hekey = key.split('\\')[0]
hkey = getattr(_winreg, hekey)
skey = '\\'.join(key.split('\\')[1:])
try:
    if archi==64:
        pkey = _winreg.OpenKey(hkey, skey,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ)
        print hekey+'\\'+skey+' exists'
        with disable_file_system_redirection():
            cmd='reg query "%s" /s'%(reg_path)
            a=os.popen(cmd).read()
            write(a)
            c=compare()
    elif archi==86:
        pkey = _winreg.OpenKey(hkey, skey)
        print hekey+'\\'+skey+' exists'
        with disable_file_system_redirection():
            cmd='reg query "%s" /s'%(reg_path)
            a=os.popen(cmd).read()
            write(a)
            c=compare()
        
except WindowsError as e:
    print e
    print 'Check whether '+hekey+'\\'+skey+' is valid or accessible!'
    c=2
    
def remove():
    os.remove(fileToSend1)
    os.rename(fileToSend2,fileToSend1)

if c==1:
    print 'YES - (Changes made in your regitry key value %s)'%(reg_path)
    alert(1)
    remove()
    print '\nThe changed registry key is available in the file at the following path  '+fileToSend1
elif c==2:
    alert(0)
else:
    print "NO - (No Changes have made in your regitry key value %s)"%(reg_path)
    alert(0)
    
