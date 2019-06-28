Folder1=r'C:\Program Files\COMODO1\COMODO Internet Security'## Here mention the folder path which you want to rename
Folder2=r'C:\Program Files\COMODO1\COMODO Internet Security123'## Here mention the folder path with new name
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
    if (os.path.exists(Folder1)):
        print 'Path exists rename has been iniitiated'
        os.rename(Folder1,Folder2)
        print 'rename successful'
    else:
        print 'No such path available'
    
