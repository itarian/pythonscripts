import _winreg
import ctypes
import os
import re

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
    val=os.popen('reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" | find /i "ProxyServer"').read()
    v=os.popen('reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" | find /i "ProxyOverride"').read()
    v=v.strip()
    val=val.strip()
    val1=re.findall("ProxyServer\s\s\s\sREG_SZ\s\s\s\s(.*)",val)
    val1=''.join(val1)
    Proxy_server_ip=re.findall("(.*):",val1)
    Proxy_server_ip=''.join(Proxy_server_ip)
    port=re.findall(":(.*)",val1)
    port=''.join(port)
    except_ip=re.findall("ProxyOverride\s\s\s\sREG_SZ\s\s\s\s(.*)",v)
    except_ip=''.join(except_ip)    
    if val1=='':
        print "There is no proxy server used in the device"
    else:
        print "The proxy server ip is "+Proxy_server_ip
        print "The port number is "+port
        if except_ip=='':
            pass
        else:
            print "The  ip addresses excluded in the proxy are "+except_ip

        

