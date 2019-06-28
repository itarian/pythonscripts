import _winreg
import os
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

handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"SYSTEM\CurrentControlSet\Control\Session Manager\Power",0,_winreg.KEY_ALL_ACCESS)
_winreg.SetValueEx(handle, "HiberbootEnabled", 0, _winreg.REG_DWORD, 0)
print "Disabling the fast start up"

