Path = r'C:\Users\Administrator\Documents\output.txt' ## Here you can specifies your files or folder 

import ctypes
import subprocess
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

if os.path.isdir(Path):
    with disable_file_system_redirection():
        pObj = subprocess.Popen('takeown /F {} /R /D N'.format(Path), shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    for i in pObj.communicate():
        print i
elif os.path.isfile(Path):
    with disable_file_system_redirection():
        pObj = subprocess.Popen('takeown /F {}'.format(Path), shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    for i in pObj.communicate():
        print i
else:
    print '{} is not valid file / folder'.format(Path)

