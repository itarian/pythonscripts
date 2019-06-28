cmd="C:\pagefile.sys 3900 4500" ##Please enter the minimum and maximum values here

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

    command='REG add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v "PagingFiles" /t REG_MULTI_SZ /d "'+cmd+'" /f'
    
    set=os.popen(command).read()
    print set
    print "The system will restart now to reflect the changes in registry"
    restart=os.popen("shutdown -r ").read()
    
