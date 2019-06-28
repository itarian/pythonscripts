registry_key=r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
reg_field="PROCESSOR_ARCHITECTURE"

import os
import _winreg

reg_key=registry_key.split(os.sep)
key = getattr(_winreg,reg_key[0])
subkey = _winreg.OpenKey(key, os.sep.join(reg_key[1:]), 0, _winreg.KEY_ALL_ACCESS)
(value, type) = _winreg.QueryValueEx(subkey,reg_field)
print value
