import os
import ctypes
import shutil
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

Dir_old="C:\Program Files\Comodo\Comodo Internet Security - old"
Dir_new="C:\Program Files\Comodo\Comodo Internet Security"
with disable_file_system_redirection():
    if os.path.isdir(Dir_old):
        os.rename(Dir_old,Dir_new)
        print "Renamed successfully...."       
    else:
        print "Folder not exists..."
