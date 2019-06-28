import os
from _winreg import *
import _winreg
key_to_read = r'SOFTWARE\\Microsoft\\PowerShell\\3\\PowerShellEngine'
key_to_read1 = r'SOFTWARE\\Microsoft\\PowerShell\\1\\PowerShellEngine'
try:
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    k = OpenKey(reg, key_to_read)
    hkey =_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, key_to_read)
    version2 = _winreg.QueryValueEx(hkey, "PowerShellVersion")
    version1='.'.join(version2[0])[0]
    print version1
except:
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    k = OpenKey(reg, key_to_read1)
    hkey1 =_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, key_to_read1)
    version2 = _winreg.QueryValueEx(hkey1, "PowerShellVersion")
    version1='.'.join(version2[0])[0]
    print version1
if int(version1) >= 4:
    out=os.popen(r'powershell.exe -executionpolicy bypass "Invoke-CimMethod -Namespace root/cis SbControl -MethodName ResetSandbox"').read();
    print(out);  
else:    
    out=os.popen(r'powershell.exe -executionpolicy bypass "Invoke-WmiMethod -Namespace root/cis SbControl -Name ResetSandbox"').read();
    print(out);
    
