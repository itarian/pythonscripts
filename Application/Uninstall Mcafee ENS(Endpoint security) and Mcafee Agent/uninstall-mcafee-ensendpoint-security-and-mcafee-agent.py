import os
import re
import random
import socket
import _winreg
from subprocess import PIPE, Popen
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

def DNDS(rtkey, pK, kA):
    ln = []
    lv = []
    lp=[]
    di=[]
    try:
        oK = _winreg.OpenKey(rtkey, pK, 0, kA)
        i = 0
        while True:
            try:
                bkey = _winreg.EnumKey(oK, i)
                vkey = os.path.join(pK, bkey)
                oK1 = _winreg.OpenKey(rtkey, vkey, 0, kA)
                try:
                    tls = []
                    DN, bla = _winreg.QueryValueEx(oK1, 'Uninstall Command')
                   
                    _winreg.CloseKey(oK1)
                    ln.append(DN)
                    
                except:
                    pass
                i += 1
            except:
                break
        _winreg.CloseKey(oK)
        return zip(ln)
    except:
        return zip(ln)
rK = _winreg.HKEY_LOCAL_MACHINE
sK = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
openedKey = _winreg.OpenKey(rK, sK, 0, _winreg.KEY_READ)
arch, bla = _winreg.QueryValueEx(openedKey, 'PROCESSOR_ARCHITECTURE')
arch = str(arch)

_winreg.CloseKey(openedKey)
def find(pattern, path):
    import os, fnmatch
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result
def agentuninstall(arch):
    if arch == 'AMD64':
        REG='SOFTWARE\WOW6432Node\Network Associates\ePolicy Orchestrator\Application Plugins'
        agentpath=r"C:\Program Files (x86)\McAfee"
       
    else:
        REG='SOFTWARE\Network Associates\ePolicy Orchestrator\Application Plugins'
        agentpath=r"c:\Program Files\McAfee"

    ki=DNDS(_winreg.HKEY_LOCAL_MACHINE,REG, _winreg.KEY_READ)
    for i in ki:
        CMD=i[0]
        ExecuteCMD(CMD)
    ki=find('*.exe',agentpath)
    if len(ki)==0:
        agentpath=r"c:\Program Files\McAfee"
        ki=find('*.exe',agentpath)    
    for i in ki:
        if "FrmInst.exe" in i:
            CMD='"'+i+'"' + " /Remove=Agent /Silent "
            ExecuteCMD(CMD)
            CMD='"'+i+'"' + " /FORCEUNINSTALL "
            ExecuteCMD(CMD)
CMD='wmic product  get name'
ki=os.popen(CMD).read()
if "McAfee Endpoint Security Platform " and  "McAfee Agent" in ki:
	print "Mcafee is installed in endpoint"
	agentuninstall(arch)
	print "Mcafee is successfully uninstalled in endpoint"
	print "System requires reboot to make the changes"
	print "System will restart in 2 mins"
	cmd=os.popen('shutdown.exe -r -t 120 /f').read()
		
else:
    print "Mcafee is not installed in endpoint"
