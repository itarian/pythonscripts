days=8    ## change the number of days, you would like to check for uptime.
t='00:01:45'  ## provide the time of delay for the restart, make sure that time is given in this format(HH:MM:SS).

import os
import ctypes
import time

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)
time1=get_sec(t)
print get_sec(t)
file=os.path.join(os.environ['SYSTEMDRIVE'], os.sep, 'checkboottime.ps1')
input="""
$os = Get-WmiObject win32_operatingsystem
$uptime = (Get-Date) - ($os.ConvertToDateTime($os.lastbootuptime))
$Display = "Windows-Endpoint Uptime in Days: " + $Uptime.days 
Write-Output $Display 
if($uptime.days -ge %s)
{
Write-Output "Time to restart the Windows-Endpoint and the Force Restart is Initiated!"
Write-Output "Restart"
}
Else
{
"No restart Required"
}
"""%(str(days))
with open(file, "w") as fobj:
    fobj.write(input)
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
    out=os.popen('powershell.exe -executionpolicy bypass -file C:\checkboottime.ps1').read()
print out
if "Restart" in out:
   print os.popen("shutdown -r -t %s"%time1).read()
