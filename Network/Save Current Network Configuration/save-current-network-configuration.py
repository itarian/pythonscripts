dat_file_path=r"C:\Users\Administrator.W10P64\Desktop\MyNetworkCFG.dat"
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
    out=os.system('netsh interface dump > "%s"'%dat_file_path)
if out==0:
    print 'The Network Config is Dumped at %s'%dat_file_path
else:
    print 'The Network Config is not Dumped'
