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
        print 'Windows Update Service is already running'
        with disable_file_system_redirection():
            print "Disabling Windows Update Service..."
            cmd1=os.popen("sc config wuauserv start= disabled").read()
            print cmd1
            cmd2=os.popen("net stop wuauserv").read()
            print cmd2
            print 'Windows Update Service is Disabled'
    elif 'STOPPED' in cmd:
        print 'Windows Update Service is already disabled'

