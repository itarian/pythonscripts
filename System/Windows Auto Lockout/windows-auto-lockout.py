#Please restart the system once to take changes effect
Thresholdvalue = 10 #here edit with your time which should be in seconds(eg: 3m=3*60=>180sec)
from _winreg import *
def modifyRegistry(key, sub_key, valueName, valueType, value):
    """
    A simple function used to change values in
    the Windows Registry.
    """
    try:
        key_handle = OpenKey(key, sub_key, 0, KEY_ALL_ACCESS)
    except WindowsError:
        key_handle = CreateKey(key, sub_key)
 
    SetValueEx(key_handle, valueName, 0, valueType, value)
    CloseKey(key_handle)
 
try:
    i = 0
    while True:
        subkey = EnumKey(HKEY_USERS, i)
        if len(subkey) > 30:
            break
        i += 1
except WindowsError:
    # WindowsError: [Errno 259] No more data is available
    # looped through all the subkeys without finding the right one
    raise WindowsError("Could not apply workstation lock settings!")
 
subkey = r'%s\Control Panel\Desktop' % subkey
data= [('ScreenSaverIsSecure', REG_DWORD, 1),
              ('ScreenSaveTimeOut', REG_SZ, '{}'.format(Thresholdvalue)),
              ('SCRNSAVE.EXE', REG_SZ, 'logon.scr')]
 
for valueName, valueType, value in data:
    modifyRegistry(HKEY_USERS, subkey, valueName, 
                   valueType, value)
 
modifyRegistry(HKEY_CURRENT_USER,
               r'Software\Microsoft\Windows\CurrentVersion\Policies\System',
               'NoDispScrSavPage', REG_DWORD, 1)

print 'ScreenSaveTimeOut has been updated sucessfully'
print 'The device will lock out after %s seconds of idleness'%(Thresholdvalue)
