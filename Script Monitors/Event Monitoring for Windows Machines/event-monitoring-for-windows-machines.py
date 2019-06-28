import os
import re
import filecmp
import difflib
import sys
import sqlite3


ps_content=r'''
Get-WinEvent -LogName System -MaxEvents 20
Get-WinEvent -LogName Security -MaxEvents 20
Get-WinEvent -LogName Setup -MaxEvents 20
Get-WinEvent -LogName Application -MaxEvents 20
'''
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
            return out.strip()
        else:
            return ret
    else:
        if err:
            return err.strip()
        else:
            return ret

file_name='powershell_file.ps1'
file_path=os.path.join(os.environ['TEMP'], file_name)
with open(file_path, 'wb') as wr:
    wr.write(ps_content)

ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
cur1=ecmd('powershell "%s"'%file_path)
##print cur1

os.remove(file_path)



workdir=os.environ['PROGRAMDATA']+r'\c1_temp'
if not os.path.exists(workdir):
    os.makedirs(workdir)
save_path=workdir
si1=[]
doll1=''
flag=0
global fnd2
fnd2=0
ot=save_path+"\\Output.txt"

cur12 = cur1.lower()
for i in [i.strip() for i in cur12.split("\n\n")  if i.strip()]:
    i = i.lower()
    si1.append(i)

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg)) 
def files():
    file_name1 = "Block_Appold.txt"
    cur_dir1 = save_path
    file_list1 = os.listdir(cur_dir1)
    parent_dir1 = os.path.dirname(cur_dir1)
    if file_name1 in file_list1:
        fnd2=1
        with open(os.path.join(save_path, "Block_Appnew"+".txt"), "w") as file21:
            for j in si1:
                j=str(j)
                file21.write(j+'\n')
                fnd2=1      
    else:
        with open(os.path.join(save_path, "Block_Appold"+".txt"), "w") as file21:
            file21.write('\n')
            fnd2=2  
    return fnd2
def swchanges():  
    file11=save_path+"\\Block_Appnew.txt"
    file21=save_path+"\\Block_Appold.txt"
    ot=save_path+"\\Output.txt"
    flag=0 
    if False==0:     
        with open(file11) as file:
           data1=file.read()
           data1.strip()
           with open(file21) as file:
               data21=file.read()
               data21.strip()
               text1Lines1 = data1.splitlines(1)
               text2Lines1 = data21.splitlines(1)
               diffInstance1 = difflib.Differ()
               diffList1 = list(diffInstance1.compare(text1Lines1,text2Lines1 ))
               with open(ot, 'a+') as o1:
                   o1.write("\n********** Newly Added Critical Event logs***********\n")
                   for line in diffList1:
                       if line[0] == '-':
                           flag=1
                           o1.write(line)
               o1.close()  
           file.close()
        file.close()
    return flag 
def remove():
    os.remove(save_path+"\\Block_Appold.txt")
    os.rename(save_path+"\\Block_Appnew.txt",save_path+"\\Block_Appold.txt" )
    os.remove(save_path+"\\Output.txt")
ki=files()
if ki==2:
    with open(os.path.join(save_path, "Block_Appold"+".txt"), "w") as file21:
        file21.write('\n')
    file21.close()
    ki=files()
s=swchanges()
if s ==0:
    print "No file has Added "
    alert(0)
else:
    with open(ot, 'r') as o1:
        for i in o1:
            print i
    o1.close()
    alert(1)
v=remove()
