import subprocess
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



#To uninstall n-able Windows Agent"

with disable_file_system_redirection():
    CMD=os.popen('wmic product where name="Windows Agent" call uninstall').read()
    
if 'ReturnValue = 0' in CMD:
    print 'successfully uninstalled n-able Windows Agent '
else:
    print'n-able Windows Agent is not installed on your endpoint'
