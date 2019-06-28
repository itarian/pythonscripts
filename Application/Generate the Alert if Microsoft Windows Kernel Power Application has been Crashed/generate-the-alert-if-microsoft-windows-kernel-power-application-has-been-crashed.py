import os 
import sys
import ctypes
import _winreg 

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg)) 

# Please use "alert(1)" to turn on the monitor(trigger an alert) # Please use "alert(0)" to turn off the monitor(disable an alert) 
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
    setpolicy=os.popen('powershell "Set-ExecutionPolicy RemoteSigned"').read()
    logs=os.popen( "powershell.exe " "Get-WinEvent -FilterHashtable @{logname='system'; providername='Microsoft-Windows-Kernel-Power'; id=41; level=1}").read()
    
    
if logs:
    print 'Application crash event has been occured'
    alert(1)
    print "Event Details"
    print logs
    
else:
    alert(0)
    print ' No application crashed found recently'


