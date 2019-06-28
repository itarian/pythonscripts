BAT='''C:
cd "C:\Program Files\McAfee\Agent\*86"
cd
FrmInst.exe /forceuninstall
'''
BAT1='''C:
cd "C:\Program Files\McAfee\Agent"
cd
FrmInst.exe /forceuninstall
'''
import os
import sys
import platform
import subprocess
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

def machine():
    """Return type of machine."""
    if os.name == 'nt' and sys.version_info[:2] < (2,7):
        return os.environ.get("PROCESSOR_ARCHITEW6432", 
               os.environ.get('PROCESSOR_ARCHITECTURE', ''))
    else:
        return platform.machine()

def os_bits(machine=machine()):
    """Return bitness of operating system, or None if unknown."""
    machine2bits = {'AMD64': 64, 'x86_64': 64, 'i386': 32, 'x86': 32}
    return machine2bits.get(machine, None)

x=(os_bits())

if x == 64:
    path=os.environ['programdata']+"\Sample.bat"
    with open(path,"w") as f:
        f.write(BAT)

    with disable_file_system_redirection():
            process = subprocess.Popen([path],stdout=subprocess.PIPE)
            stdout = process.communicate()[0]
            print "MCAfee uninstalled successfully"
else:
    path=os.environ['programdata']+"\Sample.bat"
    with open(path,"w") as f:
        f.write(BAT1)

    with disable_file_system_redirection():
            process = subprocess.Popen([path],stdout=subprocess.PIPE)
            stdout = process.communicate()[0]
            print "MCAfee uninstalled successfully"
