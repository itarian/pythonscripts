uN = 'Administrator'
pWD = 'welcome@123' ## password setup is based on policy requirement. the complex policy does not accept the simple password!
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
with disable_file_system_redirection():
    pObj = subprocess.Popen('net user "%s" "%s"'%(uN, pWD), shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
oC = pObj.communicate()
ret=pObj.returncode
if ret==0:
    print oC[0].strip()
else:
    print oC[1].strip()
