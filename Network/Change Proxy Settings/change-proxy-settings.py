proxy_IP='52.34.20.124'##give the ipaddress of your porxy
proxy_port='19080'##give the portnumber for your proxy
proxy_except='52.34.20.124;52.34.20.125;52.34.20.127'##give the ip addresses that you want to exclude use semicolon(;) to separate entries
import _winreg
import ctypes
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
handle = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,"Software\Microsoft\Windows\CurrentVersion\Internet Settings",0,_winreg.KEY_ALL_ACCESS)
_winreg.SetValueEx(handle, "ProxyEnable", 0, _winreg.REG_DWORD, 0x1)
_winreg.SetValueEx(handle, "ProxyServer", 0, _winreg.REG_SZ,proxy_IP+':'+proxy_port)
_winreg.SetValueEx(handle, "ProxyOverride", 0, _winreg.REG_SZ,proxy_except)
print "Proxy Settings Updated"
print 'Restarting the endpoint to apply changes ....'
with disable_file_system_redirection():
    val=os.popen('shutdown -r').read()
