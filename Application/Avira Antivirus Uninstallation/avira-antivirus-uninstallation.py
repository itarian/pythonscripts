import os
import re
import random
import socket
import _winreg
import re
from subprocess import PIPE, Popen
import shutil
rK = _winreg.HKEY_LOCAL_MACHINE
sK = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
openedKey = _winreg.OpenKey(rK, sK, 0, _winreg.KEY_READ)
arch, bla = _winreg.QueryValueEx(openedKey, 'PROCESSOR_ARCHITECTURE')
arch = str(arch)
def ExecuteCMD(CMD, OUT = False):
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
    from subprocess import PIPE, Popen
    with disable_file_system_redirection():
        OBJ = Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = OBJ.communicate()
    RET = OBJ.returncode
    if RET == 0:
        if OUT == True:
            if out != '':
                return out.strip()
            else:
                return True
        else:
            return True
    return False
def agentuninstall(agentpath):
        agentpath=agentpath+r"\setup.exe"
        CMD='"'+agentpath+'"' + " /remsilentnoreboot "
        ExecuteCMD(CMD, OUT = False)
            
if arch == 'AMD64':
        agentpath1=r"C:\Program Files (x86)\Avira"
        agentpath=r"C:\Program Files (x86)\Avira\Antivirus"
        if os.path.exists(agentpath):
            agentuninstall(agentpath)
            print "Avira is successfully uninstalled in endpoint"
        else:
            print "Avira is not installed in endpoint"
else:
        agentpath1=r"C:\Program Files\Avira"
        agentpath=r"C:\Program Files\Avira\Antivirus"
        if os.path.exists(agentpath):
            agentuninstall(agentpath)
            print "Avira is successfully uninstalled in endpoint"
        else:
            print "Avira is not installed in endpoint"
           

CMD='tasklist | find "Avira"'
Ki=ExecuteCMD(CMD, OUT = True)
if Ki!=False:
    Ki=re.findall("(.*).exe",Ki)
    if len(Ki)>0:
        for i in Ki:
            Taskname='"'+i+'.exe"'
            CMD=Taskname
            print ExecuteCMD(CMD, OUT = True)

import os
exe = 'Avira.OE.Setup.Bundle.exe'
for root, dirs, files in os.walk(r'C:\ProgramData\Package Cache'):
    for name in files:
        if name == exe:
            Path=os.path.abspath(os.path.join(root, name))
            
try:
    CMD='"'+Path+'"' + " /uninstall /quiet "
    ExecuteCMD(CMD)
    ExecuteCMD("shutdown /a")
except:
    pass
if os.path.exists(agentpath1):
            try:
                shutil.rmtree(agentpath1)
            except:
                pass
