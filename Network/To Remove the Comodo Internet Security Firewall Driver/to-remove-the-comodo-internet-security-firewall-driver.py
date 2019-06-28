latestversion=r"10.0.2.6408"#provide the latest version here
import os
import re
import ctypes
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
    a=os.popen('wmic product where "Name like "%Security%"" get Name, Version').read()
    b=os.popen('wmic product where "Name like "%Internet%"" get Name, Version').read()
    if a==b:
        c=re.findall("[0-9]{2}\W[0-9]{1}\W[0-9]{1}\W[0-9]{4}",a)
        cuurentversion=''.join(c)
        if latestversion>currentversion:
            print"The currently installed version is not a latest version..please update and try again"
            pass
        elif latestversion<=currentversion:
            def remove():
                Disable_service=os.popen("sc config inspect start= disabled").read()
                if Disable_service:
                    print "Inspect Driver Service %s disabled" %('.'* 10)
                else:
                    print "Driver service not enabled"
                Stop_service=os.popen("net stop inspect").read()
                if Stop_service:
                    print "The COMODO Internet Security Firewall Driver service %s stopped" %('.'* 10)
                else:
                    print "The COMODO Internet Security Firewall Driver service %s not started" %('.'* 10)
                del_driver=os.popen('reg delete "HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Network\{4d36e974-e325-11ce-bfc1-08002be10318}\{208D67BB-EF7E-4183-8341-580548FB2E4D}" /f').read()
                if del_driver:
                    print "COMODO Internet Security Firewall Driver removed from the System"
                else:
                    print "COMODO Internet Security Firewall Driver is not present at Endpoint"
            remove()
            def restart():
                with disable_file_system_redirection():
                    print "Restarting at End point to apply changes......"
                    os.popen("shutdown -r").read()
            restart()
    else:
        print "Make sure CIS is installed at endpoint"


