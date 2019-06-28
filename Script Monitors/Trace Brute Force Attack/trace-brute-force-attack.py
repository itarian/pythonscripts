no=10 ##Mention the no of log on failures after which the alert should be generated
Mins=2 ##Here mention the minutes to check for the logon failures (It should be same as monitoring time period)
Eventid=4625
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
        logs=  os.popen('powershell.exe ' + '"'+'Get-EventLog -Log "Security" -After (Get-Date).AddMinutes(-%s)'%Mins+'| where {$_.eventID -eq "%s"} | Format-List -Property *'%Eventid+'"').read()

    if logs:
        fp=os.environ['PROGRAMDATA']+"\\"+"Brute_Detection.txt"
        if os.path.exists(fp):
            with open(fp,'a+') as f:
                f.write("Hai")
                f.write("\n")
        else:
            fp=os.path.join(os.environ['PROGRAMDATA'],"Brute_Detection.txt")
            with open(fp,'a+') as f:
                f.write("Hai")
                f.write("\n")
        c=0
        with open(fp,'a+') as f:
            for i in f:
                c+=1
        if c>=no:
            print"Brute force attack detection for %s no of log on failures"%no
            f = open(fp, 'r+')
            f.truncate(0)
            alert(1)
        
    else:
        alert(0)
        print 'No application log on failure has occured'
     
eventid()
