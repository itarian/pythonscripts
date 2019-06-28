rn='"Zoo TCP Port 80"'
dr="in"
an="allow"
pl="TCP"
prt="80"
import ctypes
import subprocess
import os
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


def firewall():
   with disable_file_system_redirection():
        frwl='netsh advfirewall firewall add rule name='+rn+' '+'dir='+dr+' '+'action='+an+' '+'protocol='+pl+' '+'localport='+prt
        frwlusr=os.popen(frwl).read()
        print frwlusr
        print  'Opening a Windows Firewall Port'

firewall()
