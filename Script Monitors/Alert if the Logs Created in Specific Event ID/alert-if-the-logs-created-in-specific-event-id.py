Eventid=1002## Here mention the Event Id to get the details 
Mins=15 ##Here mention the minutes to check the crashed files (It should be same as monitoring time period) 
import os 
import sys
import ctypes
import _winreg
import ctypes

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg)) 

# Please use "alert(1)" to turn on the monitor(trigger an alert) # Please use "alert(0)" to turn off the monitor(disable an alert) 
# Please do not change above block and write your script below
def eventid():
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
        logs=  os.popen('powershell.exe ' + '"'+'Get-EventLog -Log "Application" -After (Get-Date).AddMinutes(-%s)'%Mins+'| where {$_.eventID -eq "%s"} | Format-List -Property *'%Eventid+'"').read()

    if logs:
        alert(1)
        print 'Appliacion crash event %s has been occured'%Eventid
        print "Event Details"
        print logs
        
    else:
        alert(0)
        print 'No application crashed event %s has occured'%Eventid
     
eventid()

