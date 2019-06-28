cmd1="del /s /q /f C:\*.mp4 E:\*.mp4 " # Enter the drives name as per your system
cmd2="del /s /q /f C:\*.avi E:\*.avi " # Enter the drives name as per your system

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
    OB = Popen(cmd1, shell=True, stdout = PIPE, stderr = PIPE)
RES = OB.communicate()
RET = OB.returncode
if RET == 0:
    print 'Deleted .mp4 files successfully'
else:
    print RES[1]


OB2 = Popen(cmd2, shell=True, stdout = PIPE, stderr = PIPE)
RES2 = OB2.communicate()
RET2 = OB2.returncode
if RET2 == 0:
    print 'Deleted .avi files successfully'
else:
    print RES2[1]

