import subprocess
import os
import ctypes
import platform



class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

if 'PROGRAMW6432' in os.environ.keys():
    path=r'"C:\Program Files\CCleaner\CCleaner64.exe"'
else:
    path=r'"C:\Program Files\CCleaner\CCleaner.exe"'


CMD=path+r" /AUTO"
print CMD

with disable_file_system_redirection():
    ping = subprocess.Popen(CMD,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
    out=ping.communicate()[1]
    output = str(out)
    print output
    print 'successfully runned'

