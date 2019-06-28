proxy_IP='8.8.8.8'##give the ipaddress of your porxy
proxy_port='8080'##give the portnumber for your proxy
###proxy_except=''##give the ip addresses that you want to exclude use semicolon(;) to separate entries
###For eg, proxy_except='52.34.20.124;52.34.20.125;52.34.20.127'
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

def num_there(s):
    if any(i.isdigit() for i in s):
        _winreg.SetValueEx(handle, "ProxyServer", 0, _winreg.REG_SZ,proxy_IP+':'+proxy_port)          
num_there(proxy_IP)        
    
print "Proxy Settings Updated"
print "Google chrome default search settings changed to Uk"
print 'Restarting the endpoint to apply changes ....'
with disable_file_system_redirection():
    val=os.popen('shutdown -r').read()
