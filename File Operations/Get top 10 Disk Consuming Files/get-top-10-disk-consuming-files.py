import ctypes
import sys
import os

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

print ' Top 10 files based on the size '
print ' *******************************'

with disable_file_system_redirection():
    out=os.popen( r'powershell.exe "get-ChildItem C:\ -recurse -erroraction silentlycontinue | sort length -descending | select -first 10"').read()
    print out
             
