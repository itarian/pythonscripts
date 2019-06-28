import os
import ctypes
import sys

check_shutdown = "Get-EventLog -LogName system -Source user32 -After (Get-Date).AddSeconds(-60) | select -ExpandProperty message"

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

with disable_file_system_redirection():
    setpolicy=os.popen('powershell "Set-ExecutionPolicy RemoteSigned"').read()
    run_check_shutdown = os.popen('powershell.exe ' + '"' + check_shutdown +'"').read()
    run_check_shutdown = run_check_shutdown.lower()

def check(run_check_shutdown):
    try:
        for i in [i.strip() for i in run_check_shutdown.split('\n')   if 'restart' in i or 'shutdown' in i or ' power off' in i if i.strip()]:
            if 'shutdown type:' not in i:
                alert(1)
                print 'The Event Message is : "' +i 
                print i
                print "\n"
    except Exception as error:
        pass
    
check(run_check_shutdown)

if run_check_shutdown == None or run_check_shutdown == "":
    print "No shutdown or Restart event"
    alert(0)

