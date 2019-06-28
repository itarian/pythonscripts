Service = "vds" ## Here enter the service name to restart
import ctypes
import sys
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
    
def alert(arg): 
	sys.stderr.write("%d%d%d" % (arg, arg, arg))
import os
import subprocess
with disable_file_system_redirection():
    Status_service = 'Get-Service ' +Service +' |Select-object Status'
    setpolicy=os.popen('powershell "Set-ExecutionPolicy RemoteSigned"').read()
    run_check_windows_startup = os.popen('powershell.exe ' + '"' + Status_service +'"').read()
    s=[]
    for i in [i.strip() for i in run_check_windows_startup.split('\n')  if i.strip()]:
        s.append(i)
    a=s[2:]
    b=(''.join(a))
    if "Stopped" in b:
        try:
            Start_service= 'net start '+Service
            print 'The service '+Service+' was stopped'
            print 'starting now '
            x=os.popen(Start_service).read()
            print 'The Service '+Service+' has been started'
            alert(1)
        except Exception as err: 
            print "Unable to start the Service" +Service +'due to below error'
            print err
            alert(1)       
                       
    else:
        print "The service "+Service+' is running as expected'
        alert(0)
