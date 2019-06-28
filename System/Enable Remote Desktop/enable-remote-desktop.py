from _winreg import *
aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)                                                
aKey = OpenKey(aReg, r"SYSTEM\CurrentControlSet\Control\Terminal Server", 0, KEY_ALL_ACCESS)
try:
    SetValueEx(aKey,"fDenyTSConnections",0,REG_DWORD, 0x0000)
    val=QueryValueEx(aKey, "fDenyTSConnections")
    if val[0]==0:
        print "RDP access is enabled"
except EnvironmentError:                                          
    print "Encountered problems writing into the Registry..."
CloseKey(aKey)          


