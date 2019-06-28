import _winreg
def enableUSBPort():
    openedKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Services\\USBSTOR', 0, _winreg.KEY_ALL_ACCESS)
    _winreg.SetValueEx(openedKey, 'Start', 0, _winreg.REG_DWORD, 3)
    modifiedValue = _winreg.QueryValueEx(openedKey, 'Start')[0]
    _winreg.CloseKey(openedKey)
    return modifiedValue
if __name__=='__main__':
    try:
        enableUSBPort()
        print 'USB Port is successfully enabled!'
    except Exception as e:
        print e

