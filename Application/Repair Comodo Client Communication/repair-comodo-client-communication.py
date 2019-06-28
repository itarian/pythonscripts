import os
import ctypes
import re
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
    yy=r'wmic product get name, identifyingnumber |find "COMODO Client - Communication"'
    CMD=os.popen(yy).read()
    if CMD:
        xx=re.findall("{.*}",CMD)[0]
        os.popen("msiexec /fa %s /qn"%xx).read()
        print "The comodo client communication connected"
    else:
        print "Comodo client communication is not installed in this machine"
    
    
