import os;
import ctypes
import time

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

out=os.popen('wmic computersystem get name, Domain, Manufacturer, Model, Roles /format:list').read();
out1=os.popen('wmic nic where netenabled=true get netconnectionID').read();
out2=os.popen('wmic nicconfig where IPEnabled=True get ipaddress, macaddress /format:list').read();
print(out);
print(out1);
print(out2);

