import _winreg
import os
import ctypes
import subprocess

ps_command=r'Restart-Service wuauserv'

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate",0,_winreg.KEY_ALL_ACCESS)
_winreg.DeleteValue(handle, 'WUServer')
_winreg.DeleteValue(handle, 'WUStatusServer')
print'Keys Removed Successfully'
print'Restarting Windows Update Services'

with disable_file_system_redirection():
    process=subprocess.Popen('powershell "%s"'%ps_command, shell=True, stdout=subprocess.PIPE)
result=process.communicate()
ret=process.returncode
if ret==0:
    if result[0]:
        print result[0].strip()
    else:
        print 'Windows Update Services Restarted'
        
else:
    print '%s\n%s'%(str(ret), str(result[1]))
