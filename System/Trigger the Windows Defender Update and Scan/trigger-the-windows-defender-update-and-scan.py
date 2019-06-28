command=r'"C:\Program Files\Windows Defender\MpCmdRun.exe" /SignatureUpdateAndQuickScan'
path=r'C:\Windows\Temp\MpCmdRun.txt'
import subprocess
import ctypes
import os
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
    process=subprocess.Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
result=process.communicate()
ret=process.returncode
if ret==0:
    if result[0]:
        print result[0].strip()
    else:
        print None
        
else:
    print '%s\n%s'%(str(ret), str(result[1]))

print "Update and scanning is successfully completed"
print '%s Please check here for the windows defender logs' %path
