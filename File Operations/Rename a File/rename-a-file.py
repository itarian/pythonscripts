File1=r'C:\Users\Meteor\Desktop\check.txt'## Here mention the file name with the path which is to rename
File2=r'C:\Users\Meteor\Desktop\zzz.txt'## Here new file name with the path
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
    os.rename(File1,File2)
