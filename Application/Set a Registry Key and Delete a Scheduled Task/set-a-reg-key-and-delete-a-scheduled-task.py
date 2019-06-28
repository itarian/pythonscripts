
import os
import _winreg
import ctypes
import subprocess

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
    keyVal = r'SOFTWARE\Policies\Microsoft\Windows\CloudContent'

key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE,keyVal)
_winreg.SetValueEx(key, "DisableWindowsConsumerFeatures", 0,_winreg.REG_DWORD,1)
_winreg.CloseKey(key)
print "Changes Updated Sucessfully "
a=os.popen('schtasks /Query /FO List','r',-1).read()
if "TaskName:      \Microsoft\Windows\WindowsUpdate\Automatic App Update" in a:
    process= subprocess.Popen(['SchTasks','/Delete','/TN','Microsoft\Windows\WindowsUpdate\Automatic App Update','/F'], shell=True, stdout=subprocess.PIPE)
    result=process.communicate()
    ret=process.returncode
    if ret==0:
        print result[0]
    else:
        print result[1]

else:
     print "Task schedule is not available"
    
