import os
import getpass
import ctypes
import subprocess

kk=getpass.getuser()
drive=os.environ['SYSTEMDRIVE']
temp = drive+"\\Users\\%s\\Downloads" %(kk)


task_name='COMODO WINDOWS LOCK'
task_run=temp+r'\temprun.vbs'
minute_at=5

vbs=r'''

Set oShell = WScript.CreateObject("WScript.Shell")
strHost = "google.com"
strPingCommand = "ping -n 1 -w 300 " & strHost
Dim Var

strexcute="rundll32 user32.dll,LockWorkStation" 

ReturnCode = oShell.Run(strPingCommand, 0 , True)

If ReturnCode = 0 Then
        Var=0
	
	
Else
        Var=0
	WScript.Sleep(20000)
	oShell.Run strexcute, 0 , True
       
End If

'''


class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


def runvbs(vbs):
    path1_details=temp
    if not os.path.isdir(path1_details): 
        os.mkdir(path1_details)
    with open(path1_details+r'\temprun.vbs',"w") as f :
        f.write(vbs)        
    with disable_file_system_redirection():
        print os.popen('cscript.exe "'+path1_details+r'\temprun.vbs"').read()
        print('Script execution completed successfully')
    
runvbs(vbs)

with disable_file_system_redirection():
    process= subprocess.Popen('schtasks /create /tn "%s" /tr "%s" /sc minute /mo %s /f'%(task_name, task_run, int(minute_at)), shell=True, stdout=subprocess.PIPE)
result=process.communicate()
ret=process.returncode
if ret==0:
    if result[0]:
        print result[0].strip()
    else:
        print result[0]
else:
    if result[1]:
        print result[1].strip()
    else:
        print result[1]




