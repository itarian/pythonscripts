import _winreg
import platform
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
l=[]
a=[]
l= platform.platform()

if l[9]=='0':
    k=l[:10]

else:
    k=l[:9]


if k=="Windows-7":
    a=platform.machine()
    if a[3:]=='64':
        s=a[3:]
        k=k+s


if(k=="Windows-7"):
    print k
    handle = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",0,_winreg.KEY_ALL_ACCESS)
    _winreg.SetValueEx(handle, "NoViewOnDrive", 0, _winreg.REG_DWORD, 0x4)
    print "local drive will be secured"
    print 'Restarting the endpoint to apply changes ....'
    with disable_file_system_redirection():
        val=os.popen('shutdown -r').read()
else:
    print k
    handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer",0,_winreg.KEY_ALL_ACCESS)
    _winreg.SetValueEx(handle, "NoViewOnDrive", 0, _winreg.REG_DWORD, 0x4)
    print "local drive will be secured"
    print 'Restarting the endpoint to apply changes ....'

    with disable_file_system_redirection():
        val=os.popen('shutdown -r').read()
