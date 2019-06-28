import subprocess
import ctypes
import os
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
            
system=os.environ["SYSTEMDRIVE"]            

if os.path.isfile(r'%s\Program Files (x86)\Advanced Monitoring Agent\unins000.exe'%system):
    with disable_file_system_redirection():
        cmd=system+'"\Program Files (x86)\Advanced Monitoring Agent\unins000.exe" /VERYSILENT /SILENT'
        ping = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
        out=ping.communicate()[0]
        output = str(out)
else:
    with disable_file_system_redirection():
        cmd=system+'"\Program Files\Advanced Monitoring Agent\unins000.exe" /VERYSILENT /SILENT'
        ping = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
        out=ping.communicate()[0]
        output = str(out)
        
print "Uninstalling Begins..."        
print "Successfully uninstalled Advanced Monitoring Agent"


