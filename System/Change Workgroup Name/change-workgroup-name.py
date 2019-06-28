workgroup = "Workgroup-Name" ## Provide workgroup name to change without any special character except '-'
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
    cmd=os.popen('wmic computersystem where name="%computername%" call joindomainorworkgroup name="'+workgroup+'"').read()
    print 'workgroup name changed and it going to restart'
    os.popen('shutdown -r').read()
    
    
