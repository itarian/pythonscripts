import _winreg;
import os;
key = getattr(_winreg,"HKEY_LOCAL_MACHINE")
subkey = _winreg.OpenKey(key, "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" )
(value, type) = _winreg.QueryValueEx(subkey,"PROCESSOR_ARCHITECTURE")
if value== 'AMD64' :
    out=os.popen(r'"C:\Program Files (x86)\Sophos\Sophos Anti-Virus\BackgroundScanClient.exe" {F86EBCD5-687E-40B1-800D-021062361F6C}').read();
    print(out)
else:
    out=os.popen(r'"C:\Program Files\Sophos\Sophos Anti-Virus\BackgroundScanClient.exe" {F86EBCD5-687E-40B1-800D-021062361F6C}').read();
    print(out)