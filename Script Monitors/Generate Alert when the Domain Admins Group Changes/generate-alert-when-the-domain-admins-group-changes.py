import os
import ctypes
import socket
import difflib
import re
import sys
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


name=os.environ['username']
print 'PC-NAME : '+name
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print "IP-ADDRESS : " + (s.getsockname()[0])
fileToSend1=os.path.join(os.environ['ProgramData'],'report.txt')
fileToSend2=os.path.join(os.environ['ProgramData'],'report_new.txt')


def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))

def write(c):
    fn="report.txt"    
    fn1='report_new.txt'
    if os.path.exists(fileToSend1):
        with open(fileToSend2, 'w+') as f:
                f.write(c)
               
    else:
        with open(fileToSend1, 'w+') as f:
                f.write(c)
                
    if not os.path.exists(fileToSend2):
        with open(fileToSend1, 'w+') as f:
                f.write(c)
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
        print str(len(diff2))+ ".......users has been newly added to Domain Admins group"
        for i in diff2:
            print i+ "...user has added to Domain Admins group"
    if diff3:
        c=1
        print str(len(diff3))+ ".......users has been removed from the Domain Admins group"
        for i in diff3:
            print i+ "...user has removed from Domain Admins group"
        
    return c


def remove():
    os.remove(fileToSend1)
    os.rename(fileToSend2,fileToSend1)

with disable_file_system_redirection():
    cmd='net group "Domain Admins"'
    a=os.popen(cmd).read()
    write(a)
    c=compare()
    
if c==1:
    alert(1)
    remove()
else:
    print "no new uers has been added to or removed from Domain Admins group"
    alert(0)
    
