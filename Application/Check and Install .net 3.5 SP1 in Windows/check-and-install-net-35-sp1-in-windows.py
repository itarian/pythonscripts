import os
import time
import platform
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


def dotnet35():
    with disable_file_system_redirection():
        osversion=platform.release()
        print 'windows '+osversion 
        if str(osversion)=="10":
            out=os.popen("Dism.exe  /Online /Add-Capability /CapabilityName:NetFx3~~~~ ").read()
        elif "2008" in str(osversion):
            out=os.popen(r'powershell "Import-Module ServerManager; Add-WindowsFeature as-net-framework"').read()
        elif (("8" == str(osversion)) or ("8.1" == str(osversion)) or ("2012" in str(osversion))):
            out=os.popen("Dism.exe  /Online /Enable-Feature /FeatureName:NetFx3 /All ").read()
        elif str(osversion)=="7": 
            out=os.popen("Dism.exe  /Online /Enable-Feature /FeatureName:NetFx3").read()            
        else: 
            out="Windows xp , Vista, Windows server 2003 cannot be updated"
    return(out) 


installed=0
check=''

try:
    with disable_file_system_redirection():  
	    check=os.popen(r'reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsversionoft\NET Framework Setup\NDP\v3.5" /v "Install"').readlines()
except:
    installed=0
    pass
	
string='Install    REG_DWORD    0x1'

if check == []:
 installed=0

for i in check:  
    if string in i :
        installed=1
        break
    else:
        installed=0
    
 
if installed==0:
    result=dotnet35()
    print (result)
elif installed==1:
    print('.Net 3.5 already installed in the machine')
else:
    pass
