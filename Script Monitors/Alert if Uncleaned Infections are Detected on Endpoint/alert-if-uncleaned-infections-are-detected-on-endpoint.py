import os
import sys
import subprocess
import ctypes
ps_command=r'Get-CimInstance -Namespace root/cis AvInfectedItem'
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg))\
                             
with disable_file_system_redirection():
    cmd1='powershell "Set-ExecutionPolicy RemoteSigned -force"'
    process1=os.popen(cmd1).read()
    process=subprocess.Popen('powershell "%s"'%ps_command, shell=True, stdout=subprocess.PIPE)
result=process.communicate()
ret=process.returncode
if len(result[0])>0:
    alert(1)
    print '\nThe following Uncleaned-Infections are found at your endpoint\n%s'%(result[0])
else:
    alert(0)
    print '\nNo Uncleaned Infections Found :)'
        




