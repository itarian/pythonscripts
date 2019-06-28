import subprocess
from subprocess import PIPE, Popen
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
    obj = subprocess.Popen('defrag.exe /C /D', shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()

    if err:
        print err
    else:
        print out

