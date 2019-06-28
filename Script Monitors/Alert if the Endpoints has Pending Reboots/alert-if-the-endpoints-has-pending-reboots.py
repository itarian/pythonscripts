import os 
import sys 
import _winreg
import ctypes 

def alert(arg): 
    sys.stderr.write("%d%d%d" % (arg, arg, arg)) 

# Please use "alert(1)" to turn on the monitor(trigger an alert) 
# Please use "alert(0)" to turn off the monitor(disable an alert) 
# Please do not change above block and write your script below 

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
    import _winreg;
    try:
        key = getattr(_winreg,"HKEY_LOCAL_MACHINE")
        subkey = _winreg.OpenKey(key, "SYSTEM\CurrentControlSet\Control\Session Manager" )
        (value, type) = _winreg.QueryValueEx(subkey,"PendingFileRenameOperations")
        if value != "":
            print "Reboot required"
            alert(1)
        elif value == "":
            print "No reboot required "
            alert(0)
    except:
        print "No reboot required"
