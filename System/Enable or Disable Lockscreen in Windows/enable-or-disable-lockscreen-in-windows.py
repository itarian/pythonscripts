LOCK_SCREEN=0  #Type 1 if you want to Disable Lock Screen or 0 if you want to Enable Lock Screen
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


with disable_file_system_redirection():
    handle = _winreg.CreateKeyEx(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\Policies\Microsoft\Windows\Personalization",0,_winreg.KEY_ALL_ACCESS)
    _winreg.SetValueEx(handle, "NoLockScreen", 0, _winreg.REG_DWORD, LOCK_SCREEN)
    if LOCK_SCREEN==1:
        print "Lock Screen is disabled Successfully"
    else:
        print "Lock Screen is enabled Successfully"
    
    
