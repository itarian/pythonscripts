Path = r'C:\Users\Galaxy\Desktop\output' ## Here you can specifies your file /folder path
import ctypes
import subprocess
import ctypes
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
with disable_file_system_redirection():
    if os.path.isdir(Path):
        Path = os.path.join(Path, '*')
        pObj = subprocess.Popen('compact /C /I {}'.format(Path), shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        rTup = pObj.communicate()
        rCod = pObj.returncode
        for i in rTup:
                print i
    else:
        print '{} is not valid folder'.format(Path)

