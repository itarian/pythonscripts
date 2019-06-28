path=r'C:\Users\World\Desktop\OneDriveMapper_v1.ps1' #Define Powershell file path
CMD='PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& "%s""'%(path)
import os
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
    ping = subprocess.Popen(CMD,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
    out = ping.communicate()[0]
    output = str(out)
    print output
    print"Powershell file executed successfully"
