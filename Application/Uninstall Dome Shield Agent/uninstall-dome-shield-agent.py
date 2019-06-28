import os
import ctypes
import subprocess
import re
import fnmatch
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result
Domepath=r"C:\ProgramData\Package Cache"

def run_cmd(command):
    with disable_file_system_redirection():
        process=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    
    result=process.communicate()
    ret=process.returncode
    
    if ret==0:
        return result[0]
    return False
Path=os.environ['systemdrive']
Path64=r"\Program Files (x86)\COMODO\Dome Agent"
Path32=r"\Program Files\COMODO\Dome Agent"
Path32=os.path.join(Path,Path32)
Path64=os.path.join(Path,Path64)
ret = os.system("taskkill /f /im  cDome.exe")
if (ret == 0 or ret == 128):
    c=0
ret_proxy = os.system("taskkill /f /im  cDome.Service.ProxyController.exe")
ret_watchdog = os.system("taskkill /f /im  cDome.Service.ProxyController.WatchDog.exe")
if (ret_proxy == 0 or ret_proxy == 128) and (ret_watchdog == 0 or ret_watchdog == 128):
            c=0
else:
    print "Error while closing Proxy Services with return code : " + str(ret_proxy)
if os.path.exists(Path32):
    print "Comodo Dome agent is installed on endpoint"
    regdel='reg delete "HKLM\SOFTWARE\COMODO\Dome Agent\config" /va /f'
    regde2='reg delete "HKLM\SOFTWARE\COMODO\Dome Agent\config" /va /f'
    run_cmd(regdel)
    run_cmd(regde2)
    ki=find('*.exe',Domepath)
    for i in ki:
        if "cDomeAgentBundle.exe" in i:
            Path='"'+i+'"'
            Scmd=" /uninstall /quiet"
            CMD=Path+Scmd
            print "Started installation ..."
            run_cmd(CMD)
            print "Uninstallation successful"
elif  os.path.exists(Path64):
    print "Comodo Dome agent is installed on endpoint"
    regdel='reg delete "HKLM\SOFTWARE\WOW6432Node\COMODO\Dome Agent\config" /va  /f'
    regde2='reg delete "HKLM\SOFTWARE\WOW6432Node\COMODO\Dome Agent\config" /va /f'
    run_cmd(regdel)
    run_cmd(regde2)
    ki=find('*.exe',Domepath)
    for i in ki:
        if "cDomeAgentBundle.exe" in i:
            Path='"'+i+'"'
            Scmd=" /uninstall /quiet"
            CMD=Path+Scmd
            print "Started Uninstallation ..."
            run_cmd(CMD)
            print "Uninstallation successful"
else:
    print "Comodo Dome not installed on endpoint"

try:
    shutil.rmtree(Path64)
except:
    pass
try:
    shutil.rmtree(Path32)
except:
    pass
