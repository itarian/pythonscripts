import _winreg
import os
import ctypes
import platform
import subprocess
import time
from threading import Thread


class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

def os_platform():
    true_platform = os.environ['PROCESSOR_ARCHITECTURE']
    try:
            true_platform = os.environ["PROCESSOR_ARCHITEW6432"]
    except KeyError:
            pass
            #true_platform not assigned to if this does not exist
    return true_platform

ki=os_platform()
archi=int(filter(str.isdigit, ki))
systm=os.environ["SYSTEMDRIVE"]

def trend():
    drive= os.environ['SystemDrive']
    if archi == 64:
        CMD=systm+r'"\Program Files (x86)\Trend Micro\OfficeScan Client\ntrmv.exe" -980223 -331'
        with disable_file_system_redirection():
            ping = subprocess.Popen(CMD,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
            out=ping.communicate()[0]
            output = str(out)
    else:
        CMD=systm+r'"\Program Files\Trend Micro\OfficeScan Client\ntrmv.exe" -980223 -331'
        with disable_file_system_redirection():
            ping = subprocess.Popen(CMD,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
            out=ping.communicate()[0]
            output = str(out)
          

trend()
time.sleep(600)
print "Trend micro office scan uninstalled successfully"
print 'Restarting the endpoint to apply changes ....'
val=os.popen('shutdown -r').read()
