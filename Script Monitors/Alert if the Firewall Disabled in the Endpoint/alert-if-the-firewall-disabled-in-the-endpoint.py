import os 
import sys 
import _winreg 

def alert(arg): 
    sys.stderr.write("%d%d%d" % (arg, arg, arg)) 

# Please use "alert(1)" to turn on the monitor(trigger an alert) 
# Please use "alert(0)" to turn off the monitor(disable an alert) 
# Please do not change above block and write your script below 

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
    def firewall():
        current_status=os.popen('Netsh Advfirewall show allprofiles').read()
        status_verify =  [i.strip() for i in current_status.split('\n') if   "OFF" in i.strip()]
        for i  in status_verify:
            print ""
        if "OFF"  in i :
            print "Firewall disabled"
            alert(1)
        elif i == "":
            print "Firewall enabled"
            alert(0)


    firewall()
