command='msiexec /i patch_agent.msi /qn AGENTUSERNAME=agent_57dfc372d8e7187e80813def PASSWORD=9251f8493e283f577480f1c7ad9c09f9 CUSTOMER=57dfc372d8e7187e80813def IPADDRESS=staging.patch.comodo.com'
url='https://patch.comodo.com/agents/patch_agent.msi'

import urllib
import os
import time
import subprocess
import ctypes
import platform


temp=os.environ['TEMP']

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

#Download Agent 


def downloadFile(DownTo, fromURL):
    try:
        fileName = fromURL.split('/')[-1]
        DownTo = os.path.join(DownTo, fileName)
        with open(DownTo, 'wb') as f:
            f.write(urllib.urlopen(fromURL).read())
        if os.path.isfile(DownTo):
            return '{} - {}KB'.format(DownTo, os.path.getsize(DownTo)/1000)
    except:
        return 'Please Check URL or Download Path!'


print dotnet35()
print downloadFile(temp,url)



os.chdir(temp)
try:
    installpatch = os.popen(command).read()
    print  'Great! Comodo One Patch Management Agent got Installed  Successfully'
except Exception as e:
    print e

print installpatch 

if 'PROGRAMW6432' in os.environ.keys():
    rule1='netsh advfirewall firewall add rule name="patch_service_1" profile=domain,private protocol=any enable=yes DIR=In program="C:\Program Files (x86)\Comodo\Comodo One Patch Management Agent\Agent.RV.Service.exe" Action=Allow'
    rule2='netsh advfirewall firewall add rule name="patch_service_1" profile=domain,private protocol=any enable=yes DIR=In program="C:\Program Files (x86)\Comodo\Comodo One Patch Management Agent\Agent.RV.WatcherService.exe" Action=Allow'
else:
    rule1='netsh advfirewall firewall add rule name="patch_service_1" profile=domain,private protocol=any enable=yes DIR=In program="C:\Program Files\Comodo\Comodo One Patch Management Agent\Agent.RV.Service.exe" Action=Allow'
    rule2='netsh advfirewall firewall add rule name="patch_service_1" profile=domain,private protocol=any enable=yes DIR=In program="C:\Program Files\Comodo\Comodo One Patch Management Agent\Agent.RV.WatcherService.exe" Action=Allow'
    

process2=subprocess.Popen((rule1),shell=True,stdout=subprocess.PIPE);
result=process2.communicate()[0]

process3=subprocess.Popen((rule2),shell=True,stdout=subprocess.PIPE);
result=process3.communicate()[0]


