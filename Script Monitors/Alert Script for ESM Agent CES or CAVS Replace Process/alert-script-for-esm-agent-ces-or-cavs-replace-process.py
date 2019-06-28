# The script is a template to check UAC status on device.
# Please use "alert(1)" to turn on the monitor(trigger an alert)
# Please use "alert(0)" to turn off the monitor(disable an alert)
# Please do not change above block and write your script below

ESM = "COMODO ESM Agent"
CES = "COMODO Endpoint Security"
CCS = "COMODO Client - Security"
CAVS = "COMODO Antivirus for Servers"
# Version = "If CES has the name COMODO Client - Security add the version here"
Version = "8.3.0.5204"

import os
import ctypes
import sys

try:
    import winreg as _winreg
except ImportError:
    try:
        import _winreg
    except ImportError:
        pass


def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))


class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection

    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))

    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


with disable_file_system_redirection():
    guid = os.popen(
        'wmic product get name,version| findstr /i /c:"COMODO Endpoint Security" /c:"COMODO ESM Agent" /c:"COMODO Antivirus for Servers" /c:"COMODO Client - Security"| sort').read()

print(guid)


def verify(keyval):
    try:
        reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
        ok = _winreg.OpenKey(reg, keyval, 0, _winreg.KEY_WOW64_32KEY | _winreg.KEY_READ)
        _winreg.CloseKey(ok)
        print("Key is present in register")
        return True
    except:
        print("Key isn't present in register")
        return False


if verify("SYSTEM\\ComodoIamOff"):
    alert(0)
else:
    print("I wasn't stopped")
    if guid:
        if (guid.find(ESM) != -1) or (guid.find(Version) != -1) or (guid.find(CAVS) != -1):
            print('ESM or CES or CAVS is present')
            alert(1)
        elif guid.find(CCS) != -1:
            print('ESM or CES is NOT present and CCS is present')
            alert(0)
    else:
        print("No CCS OR CES OR CESM Installed in the system.")
        alert(1)

