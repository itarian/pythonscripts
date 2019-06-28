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
            
print "Lists all the available windows Features and its state"
cmd='DISM /online /get-features /format:table | find "Enabled" | more'
cmd1='DISM /online /get-features /format:table | find "Disabled" | more'

with disable_file_system_redirection():
    print "Enabled windows features were:"    
    cmd=os.popen(cmd).read()
    print cmd
    print "Disabled windows features were:"
    cmd1=os.popen(cmd1).read()
    print cmd1
