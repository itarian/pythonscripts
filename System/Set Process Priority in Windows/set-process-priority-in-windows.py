app_name=r'"OfficeClickToRun.exe"'                   # please enter the process name
ProcessIDLevel=r'"high priority"'            # please enter the Priority 
import os
import ctypes
import subprocess
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
    cmd="wmic process where name="+app_name+ " CALL setpriority " + ProcessIDLevel
    ping = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
    out=ping.communicate()[0]
    print out
    val="ReturnValue = 0;"
    if val in out:
        print "Set Process  Priority"
    
