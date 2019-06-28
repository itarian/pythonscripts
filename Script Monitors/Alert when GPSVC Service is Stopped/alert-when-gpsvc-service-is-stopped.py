import os
import ctypes
import sys

def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))

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
    cmd=os.popen('sc query gpsvc | findstr /i "state"').read()
    print cmd

if "STOPPED" in cmd:
    print "gpsvc Service is stopped"
    print "Service will be started"
    cmd2=os.popen('net start gpsvc').read()
    alert(1)
else:
    print "gpsvc service is running"
    alert(0)
    
