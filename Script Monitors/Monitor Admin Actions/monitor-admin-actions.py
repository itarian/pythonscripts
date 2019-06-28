import os
import subprocess
from subprocess import PIPE, Popen
import sys
import difflib

g=0
def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg))
   
try:
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.exists(workdir):
        os.mkdir(workdir)      
except:
    workdir=os.environ['SYTEMDRIVE']

path1= os.path.join(workdir, "1new.txt")
path2=os.path.join(workdir, "2new.txt")
path3=os.path.join(workdir, "3new.txt")
path11= os.path.join(workdir, "1old.txt")
path22=os.path.join(workdir, "2old.txt")
path33=os.path.join(workdir, "3old.txt")

def remove():
    os.remove(path11)
    os.remove(path22)
    os.remove(path33)
    os.rename(path1,path11)
    os.rename(path2,path22)
    os.rename(path3,path33)

def remove1():
    os.rename(path1,path11)
    os.rename(path2,path22)
    os.rename(path3,path33)

def swchanges(file1, file2):
    flag=0
    if False==0:
        
        with open(file1) as file:
           data=file.read()
           with open(file2) as file:
               data2=file.read()
               text1Lines = data.splitlines(1)
               text2Lines = data2.splitlines(1)
               diffInstance = difflib.Differ()
               diffList = list(diffInstance.compare(text1Lines,text2Lines ))
               for line in diffList:
                 if line[0] == '-':
                     flag=1
                     break
               diffList = list(diffInstance.compare(text2Lines, text1Lines))
               for line in diffList:
                 if line[0] == '-':
                     flag=1
                     
        return flag
    

def ecmd(command):
    import ctypes
    from subprocess import PIPE, Popen
    
    class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
    
    with disable_file_system_redirection():
        obj = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()
    ret=obj.returncode
    if ret==0:
        if out:
            pass
    else:
        if err:
            print err

eid=4672
cmd="wevtutil qe Security /f:text /q:*[System/EventID=%s]   /rd:true /c:1 > %s" %(eid, path1)
ecmd(cmd)
eid=4688
cmd="wevtutil qe Security /f:text /q:*[System/EventID=%s]   /rd:true /c:1 > %s" %(eid, path2)
ecmd(cmd)
eid=4648
cmd="wevtutil qe Security /f:text /q:*[System/EventID=%s]   /rd:true /c:1 > %s" %(eid, path3)
ecmd(cmd)

if os.path.isfile(path11) and os.path.isfile(path22) and os.path.isfile(path33):
    s=swchanges(path1, path11)
    if s==0:
        print '\n*)NO, "UAC AUTHOURIZED TO THE LOGON USER"\n'
    else:
        g+=1
        print "\n*)UAC AUTHOURIZED TO THE LOGON USER\n"
        with open(path1, 'r') as fr:
            for i in fr:
                if not i:
                    pass
                else:
                    print i
            print "-----------------------------------------------------------"
    s=swchanges(path2, path22)
    if s==0:
        print '*)NO, "A new process has been created/recorded in the audit process tracking"\n'
    else:
        g+=1
        print "*)A new process has been created/recorded in the audit process tracking\n"
        with open(path2, 'r') as fr:
            for i in fr:
                if not i:
                    pass
                else:
                    print i
            print "-----------------------------------------------------------"
    s=swchanges(path3, path33)
    if s==0:
        print '*)NO,"Usage of user account with admin rights"\n'
    else:
        g+=1
        print "*)Usage of user account with admin rights\n"
        with open(path3, 'r') as fr:
            for i in fr:
                if not i:
                    pass
                else:
                    print i
            print "-----------------------------------------------------------"
    if g > 0:
        alert(1)
    else:
        alert(0)
    remove()
        
else:
    
    alert(0)
    print "This is the first time you run this monitor. You will be notified for future alert"
    remove1()
