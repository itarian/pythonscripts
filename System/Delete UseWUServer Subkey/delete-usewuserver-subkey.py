import os
import ctypes
path="HKLM\Software\Policies\Microsoft\Windows\WindowsUpdate\AU"  #path of registry
Key="UseWUServer" #key value

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


CMD=r'reg delete "%s\%s"   /f'%(path,Key)
with disable_file_system_redirection():
    out=os.popen(CMD).read()
    print out 
if len(out):
    c=0
else:
    print "Registry path Doesn't exist" 
