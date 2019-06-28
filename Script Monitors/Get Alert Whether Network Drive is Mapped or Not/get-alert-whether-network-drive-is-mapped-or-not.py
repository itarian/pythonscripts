DriveLetter = 'P: ' # Enter the Drive letter to check the mapping Status.
import os 
import sys 
import _winreg 

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg)) 

# Please use "alert(1)" to turn on the monitor(trigger an alert) 
# Please use "alert(0)" to turn off the monitor(disable an alert) 
# Please do not change above block and write your script below 

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
import os
import subprocess
   
a=os.popen("net use").read()
print "Mapped Drives are : \n"
print a

if DriveLetter in a: 
    print("Already Drive is mapped and available")
    alert(0)

else:
    print("Drive is not mapped")
    alert(1)

