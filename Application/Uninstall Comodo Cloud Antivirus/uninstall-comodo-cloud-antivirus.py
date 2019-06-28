import os
import ctypes
import time
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

system= os.environ['SystemDrive']
CMD=system+r'"\ProgramData\Comodo\CCAV\installer\ccavstart.exe" /quiet'

with disable_file_system_redirection():
    
    if os.path.isfile(r"%s\ProgramData\Comodo\CCAV\installer\ccavstart.exe" %system):
        ping = subprocess.Popen(CMD,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
        print 'uninstalling comodo cloud antivirus begins.......'
        out=ping.communicate()[0]
        output = str(out)
        print output
    else:
        print 'Comodo Cloud Antivirus does not available in your system'
time.sleep(20)        
print 'Comodo Cloud Antivirus successfully uninstalled from your system'
