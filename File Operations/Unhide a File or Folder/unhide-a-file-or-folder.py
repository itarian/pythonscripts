PATH = 'C:\\Path_To_Unhide'

import ctypes
import os
from subprocess import Popen, PIPE

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

if os.path.exists(PATH):   
    with disable_file_system_redirection():
        OBJ = Popen('attrib -H '+PATH, stdin = PIPE, stdout = PIPE, stderr = PIPE, shell=True)
    RES = OBJ.communicate()
    RET = OBJ.returncode
    if RET == 0:
        print PATH+' is unhidden successfully'
    else:
        print RES[1]
else:
    print '1: Sorry! Given path is not available.'
