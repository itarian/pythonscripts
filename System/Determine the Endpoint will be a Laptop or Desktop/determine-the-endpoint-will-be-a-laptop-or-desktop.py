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
            

def computername():
    return os.environ['COMPUTERNAME']

with disable_file_system_redirection():
    try:
        command=os.popen('WMIC Path Win32_Battery Get BatteryStatus').read()
        if "BatteryStatus" in command:
            print ' %s is a Laptop Computer' % (computername())
        else:
            print ' %s is a Desktop Computer' % (computername())
    except Exception as err:
        print "Operation failed due to the below error"
        print err
