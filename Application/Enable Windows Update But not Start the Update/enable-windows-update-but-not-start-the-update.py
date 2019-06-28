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

print 'Checking windows update service status in you system...'
with disable_file_system_redirection():
    cmd=os.popen('sc query "wuauserv" | findstr STATE').read()
    if 'RUNNING' in cmd:
        print 'Windows Update Service is already enabled'
        with disable_file_system_redirection():
            print "Stopping the Windows Update Service..."
            cmd1=os.popen("net stop wuauserv").read()
            print cmd1
            print 'Windows Update Service is enabled and it is in Stop state'
    elif 'STOPPED' in cmd:
        print 'Windows Update Service is already disabled'
        with disable_file_system_redirection():
            print "Enabling Windows Update Service..."
            cmd2=os.popen("sc config wuauserv start= auto").read()
            print cmd2
            print "Windows Update Service is Enabled and it is in stop state"
    
    
