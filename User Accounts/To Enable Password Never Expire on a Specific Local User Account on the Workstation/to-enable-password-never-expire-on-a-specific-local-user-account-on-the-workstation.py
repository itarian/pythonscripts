user ="xxxx"  #please give the local user name
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

CMD="Set-LocalUser -Name "+user+" -PasswordNeverExpires 1"
with disable_file_system_redirection():
    process=os.popen('powershell "%s"'%CMD,).read()
    print process




    
