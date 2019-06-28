import os
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
    drive= os.environ['SystemDrive']
    if os.path.isfile(r'%s\Program Files\CCleaner\uninst.exe'%drive):
        print 'uninstalling CCLeaner removal.......'
        os.popen(r'"%s\Program Files\CCleaner\uninst.exe"/S'%drive).read()
        print "uninstall"
