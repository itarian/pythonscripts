import _winreg
import subprocess
aKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"SYSTEM\CurrentControlSet\Control\Terminal Server",0,_winreg.KEY_ALL_ACCESS)
a= _winreg.QueryValueEx(aKey, 'fDenyTSConnections')[0]
if a==0:
    print "RDP already ENABLED"
else:
    print "Enabling RDP......................."
    _winreg.SetValueEx(aKey, "fDenyTSConnections", 0, _winreg.REG_DWORD, 0)
    b= _winreg.QueryValueEx(aKey, 'fDenyTSConnections')[0]
    if b==0:
        print "RDP ENABLED"
    else:
        print "RDP NOT ENABLED"
