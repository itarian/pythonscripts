reg_path=['xxxxxxxxxxxxxxxxxxx','yyyyyyyyyyyyyyyyyyyyyyy'] #edit with your registry path here
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


name=os.environ['username']
print 'PC-NAME : '+name
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print "IP-ADDRESS : " + (s.getsockname()[0])
fileToSend1=os.path.join(os.environ['ProgramData'],'registry.txt')
fileToSend2=os.path.join(os.environ['ProgramData'],'new_registry.txt')

def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))

def compare1():
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
        print "The following are the changed regisgtry values "
        print diff2
        c=1
    if diff3:
        c=1
    
    return c

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
def remove():
    os.remove(fileToSend1)
    os.rename(fileToSend2,fileToSend1)

m=len(reg_path)
s=0
import _winreg 
with disable_file_system_redirection():
    for i in reg_path:
        if m>1:
            if i==reg_path[0]:
                cmd='reg query "%s" /s'%i
                a=os.popen(cmd).read()
                if not a:
                    print "The particular path is unavailable - %s , Please provide a valid path" %i
                    
                else:
                    if os.path.exists(fileToSend1):
                        with open(fileToSend2, 'a+') as f:
                            f.write(a)
                    if not (os.path.exists(fileToSend1) and os.path.exists(fileToSend2)):
                        with open(fileToSend2, 'a+') as f:
                            f.write(a)
                        with open(fileToSend1, 'a+') as f:
                            f.write(a)
            else:
                cmd='reg query "%s" /s'%i
                a=os.popen(cmd).read()
                if not a:
                    print "The path is unavailable - %s , Please provide a valid path" %i
                else:
                    if (os.path.exists(fileToSend1) and os.path.exists(fileToSend2)):
                        n=compare()
                        if n==0:
                            with open(fileToSend2, 'a+') as f:
                                f.write(a)
                            with open(fileToSend1, 'a+') as f:
                                f.write(a)
                        elif n==1:
                            with open(fileToSend2, 'a+') as f:
                                f.write(a)
        else:
            cmd='reg query "%s" /s'%i
            a=os.popen(cmd).read()
            if not a:
                print "The path is unavailable - %s , Please provide a valid path" %i
                
            else:
                if os.path.exists(fileToSend1):
                    with open(fileToSend2, 'a+') as f:
                        f.write(a)
                if not (os.path.exists(fileToSend1) and os.path.exists(fileToSend2)):
                    with open(fileToSend2, 'a+') as f:
                        f.write(a)
                    with open(fileToSend1, 'a+') as f:
                        f.write(a)
if (os.path.exists(fileToSend1) and os.path.exists(fileToSend2)):
    s=compare1()
    if s==1:
        print 'YES - (Changes made in your regitry key value)'
        alert(1)
        remove()
        
    else:
        print "NO - (No Changes have made in your regitry key value)"
        alert(0)
        remove()  
else:
    alert(0)
  
