import os
import platform
import ctypes
from _winreg import *


class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)



key_to_read =r'Software\Policies\Microsoft\Windows\WindowsUpdate\AU'
cmd1= "REG ADD HKLM\Software\Policies\Microsoft\Windows\WindowsUpdate\AU  /v UseWUServer /t REG_DWORD /d 0 /f"
   
try:
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    k = OpenKey(reg, key_to_read)

    with disable_file_system_redirection():
        disable_ac_1 = os.popen(cmd1).read()
        print disable_ac_1
        print 'Successfully removed wsus server value'

except:
    print'WSUS server value does not exist on your end point'








