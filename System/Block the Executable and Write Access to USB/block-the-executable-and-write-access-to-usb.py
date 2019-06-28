import os
import ctypes
import _winreg
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
    
    handle = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE,"Software\Policies\Microsoft\Windows\RemovableStorageDevices\{53f5630d-b6bf-11d0-94f2-00a0c91efb8b}")
    _winreg.SetValueEx(handle, "Deny_Execute",0, _winreg.REG_DWORD, 1)
    print'USB executables blocked'

    handle1 = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE,"Software\Policies\Microsoft\Windows\RemovableStorageDevices\{53f5630d-b6bf-11d0-94f2-00a0c91efb8b}")
    _winreg.SetValueEx(handle, "Deny_Write",0, _winreg.REG_DWORD, 1)
    print'USB configuration changed to read only'
