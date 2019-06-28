metric= '77'## mention the metric value to change
index= '1' ## mention the index to change the corresponding metric
import os
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
get = "Get-NetIPInterface"
command ="Set-NetIPInterface -InterfaceIndex %s -InterfaceMetric %s"%(index,metric)
with disable_file_system_redirection():
    setpolicy=os.popen('powershell "Set-ExecutionPolicy RemoteSigned"').read()
    exe= os.popen("Powershell.exe "+command).read()
    clear= os.popen("Powershell.exe "+ get ).read()
    print clear
    print "Metric changed successfully"
