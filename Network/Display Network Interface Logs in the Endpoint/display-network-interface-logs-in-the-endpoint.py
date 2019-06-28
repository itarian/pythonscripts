import os 
import sys
import ctypes
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
get = "Get-NetIPInterface"
with disable_file_system_redirection():
    setpolicy=os.popen('powershell "Set-ExecutionPolicy RemoteSigned"').read()
    logs=os.popen( "powershell.exe   "+get ).read()
    print logs
    
