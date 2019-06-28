import os
import platform
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
    cmd0=os.popen('powercfg /hibernate on')
    print 'Enabling the windows startup sound'
    cmd=os.popen('reg add "HKEY_CURRENT_USER\AppEvents\EventLabels\SystemExit" /v ExcludeFromCPL /t REG_DWORD /d 0 /f"').read()
    cmd1=os.popen('reg add "HKEY_CURRENT_USER\AppEvents\EventLabels\WindowsLogoff" /v ExcludeFromCPL /t REG_DWORD /d 0 /f"').read()
    cmd2=os.popen('reg add "HKEY_CURRENT_USER\AppEvents\EventLabels\WindowsLogon" /v ExcludeFromCPL /t REG_DWORD /d 0 /f"').read()
    cmd3=os.popen('reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI\BootAnimation" /v DisableStartupSound /t REG_DWORD /d 0 /f"').read()
    cmd4=os.popen('shutdown -r')
  
