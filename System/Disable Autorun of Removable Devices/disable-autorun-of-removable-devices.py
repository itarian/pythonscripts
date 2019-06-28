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
handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",0,_winreg.KEY_ALL_ACCESS)
_winreg.SetValueEx(handle, "NoDriveTypeAutoRun", 0, _winreg.REG_DWORD, 0x4)
print "Auto run disabled for Removable Devices"
print 'Restarting the endpoint to apply changes ....'

with disable_file_system_redirection():
    val=os.popen('shutdown -r').read()
