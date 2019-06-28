#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('parameterName') with that parameter's name
import _winreg
Key= r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" ## Here give the registry Key path. STRING
Sub_Key= "NoAutoRebootWithLoggedOnUsers" ## Here give the sub Key of the registry. STRING
Field= _winreg.REG_DWORD ##Here give the field of it
value = 1 ##Mention the value 

import os
from _winreg import *
try:
    Key=r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU"
    if not os.path.exists(Key):
        key = _winreg.CreateKey(HKEY_LOCAL_MACHINE,Key)
    Registrykey= OpenKey(HKEY_LOCAL_MACHINE,Key, 0,KEY_WRITE)
    _winreg.SetValueEx(Registrykey,Sub_Key,0,Field,value)
    CloseKey(Registrykey)
    print "Successfully created"
except WindowsError:
    print "Error"
