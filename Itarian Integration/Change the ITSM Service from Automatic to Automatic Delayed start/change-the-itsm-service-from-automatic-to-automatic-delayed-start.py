import _winreg
handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"SYSTEM\CurrentControlSet\services\ITSMService",0,_winreg.KEY_ALL_ACCESS)
_winreg.SetValueEx(handle, "DelayedAutostart", 0, _winreg.REG_DWORD, 0x1)
print "ITSMService Successfully changed from Automatic to Automatic Delayed Start"
print 'Please Restart the system to apply changes ....'
