import ctypes
import subprocess

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
 
pObj = subprocess.Popen('wmic bios list full', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
rTup = pObj.communicate()
rCod = pObj.returncode
if rCod == 0:
    print rTup[0]
else:
    print rTup[1]
