connection_name='TestVPNConnection'
server_address='10.108.51.211'

import os
import ctypes
from subprocess import PIPE, Popen

def ecmd(command, output=False):
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
        objt = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = objt.communicate()
    ret=objt.returncode
    if not output:
        return ret
    else:
        return '%s\n%s'%(out, err)

vpn=ecmd('powershell "Add-VpnConnection -Name \"%s\" -ServerAddress \"%s\" -PassThru"'%(connection_name, server_address), True)
print vpn
