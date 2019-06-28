import os
import re
import filecmp
import difflib
import sys
import ctypes
Eventid=4625
workdir=os.environ['PROGRAMDATA']+r'\c1_temp'
if not os.path.exists(workdir):
    os.makedirs(workdir)
save_path=workdir

cmd=os.popen("systeminfo | findstr OS").read()

def eventid():
    class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
                
    setpolicy=os.popen('powershell "Set-ExecutionPolicy RemoteSigned"').read()

    if "Server" in cmd:
       with disable_file_system_redirection():
          logs=os.popen('powershell.exe ' +'"'+'Get-Eventlog security| where {$_.eventid -like %s} | select -first 1 '%Eventid+'"').read()

    elif "Microsoft Windows" in cmd:
       with disable_file_system_redirection():
         logs=os.popen('powershell.exe ' +'"'+"Get-WinEvent -FilterHashtable @{logname='application'; providername='Microsoft-Windows-EventSystem'; id=%s;}| select -first 1"%Eventid+'"').read()

    return logs

login_event=[]
flag=0
global fnd2
fnd2=0
out=save_path+"\\Output.txt"
event=eventid()

for i in [i.strip() for i in event.split("\n\n")  if i.strip()]:
    i = i.lower()
    login_event.append(i)

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg)) 
def files():
    file_name1 = "login_old.txt"
    cur_dir1 = save_path
    file_list1 = os.listdir(cur_dir1)
    parent_dir1 = os.path.dirname(cur_dir1)
    if file_name1 in file_list1:
        fnd2=1
        with open(os.path.join(save_path, "login_new.txt"), "w") as file_1:
            for j in login_event:
                j=str(j)
                file_1.write(j+'\n')
                fnd2=1      
    else:
        with open(os.path.join(save_path, "login_old.txt"), "w") as file_1:
            file_1.write('\n')
            fnd2=2  
    return fnd2
def swchanges():  
    file11=save_path+"\\login_new.txt"
    file_1=save_path+"\\login_old.txt"
    flag=0 
    if False==0:     
        with open(file11) as file:
           data1=file.read()
           data1.strip()
           with open(file_1) as file:
               data21=file.read()
               data21.strip()
               text1Lines1 = data1.splitlines(1)
               text2Lines1 = data21.splitlines(1)
               diffInstance1 = difflib.Differ()
               diffList1 = list(diffInstance1.compare(text1Lines1,text2Lines1 ))
               with open(out, 'a+') as o1:
                   o1.write("\n********** Newly Added Event logs***********\n")
                   for line in diffList1:
                       if line[0] == '-':
                           flag=1
                           o1.write(line)
               o1.close()  
           file.close()
        file.close()
    return flag 
def remove():
    os.remove(save_path+"\\login_old.txt")
    os.rename(save_path+"\\login_new.txt",save_path+"\\login_old.txt" )
    os.remove(save_path+"\\Output.txt")
ki=files()
if ki==2:
    with open(os.path.join(save_path, "login_old.txt"), "w") as file_1:
        file_1.write('\n')
    file_1.close()
    ki=files()
s=swchanges()
if s ==0:
    print "No new event for logon failed"
    alert(0)
else:
    with open(out, 'r') as o1:
        for i in o1:
            print i
    o1.close()
    alert(1)
v=remove()
