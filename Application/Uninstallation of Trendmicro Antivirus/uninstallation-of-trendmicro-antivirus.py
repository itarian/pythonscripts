import subprocess
import os
import ctypes

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
drive= os.environ['SystemDrive']
c=os.path.join(drive,os.sep,"Program Files","Trend Micro","Titanium")
if os.path.isdir(c):
    print 'Uninstalling Trend Micro Antivirus ......'
    print '\n'
    def ecmd(CMD, r=True):
        import ctypes
        from subprocess import PIPE, Popen
        with disable_file_system_redirection():
            OBJ = Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
        out, err = OBJ.communicate()
        ret=OBJ.returncode
        if r:
            return ret
        else:            
            if ret==0:
                return out
            else:
                return ret
    f=os.path.join(c, 'ForceRemove.bat')    
    ecmd(f, False)
    print 'Trend Micro, uninstalled successfully form your system'
else:
    print 'Failed to uninstall Trend Micro form your system'

systm=os.environ["SYSTEMDRIVE"]
CMD=systm+r'"\Program Files\Trend Micro\AirSupport\Uninstall.exe" /quiet'
with disable_file_system_redirection():
    
    ping = subprocess.Popen(CMD,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
    out=ping.communicate()[0]
    output = str(out)
