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
handle =_winreg.OpenKey(_winreg.HKEY_CURRENT_USER,"Software\Microsoft\OneDrive",0,_winreg.KEY_ALL_ACCESS)
_winreg.SetValueEx(handle, "TeamSiteSyncPreview", 0, _winreg.REG_DWORD, 0x1)
print "Registry patch applied successfully"
os.popen('Taskkill /IM groove.exe /F').read()
f1='C:\Program Files (x86)\Microsoft Office\root\Office16\groove.exe'
f2='C:\Program Files (x86)\Microsoft Office\root\Office16\groove.old'
os.rename(f1,f2)
print('Rename the Groove completed sucessfully')
print 'Restarting the endpoint to apply changes ....'
with disable_file_system_redirection():
    val=os.popen('shutdown -r').read()
