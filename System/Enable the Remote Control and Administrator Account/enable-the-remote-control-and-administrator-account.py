admin_pwd='comodo1' ## Set new password to administrator 
import os
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

cmd1='netsh advfirewall firewall set rule group="remote desktop" new enable=Yes'
cmd2='reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f'
cmd='net user administrator /active:yes'
with disable_file_system_redirection():
        print "Enabling the remote connection"
        remote= os.popen(cmd2).read()
        print remote
        print "Setting up firewall for remote connection..."
        firewall = os.popen(cmd1).read()
        print firewall
        print "Enabling administrator account"
        enable= os.popen(cmd).read()
        print enable
        print "Setting up password for administrator account"
        psw1 = os.popen('net user administrator "%s"'%admin_pwd).read()
        print psw1
        print 'Restarting the endpoint to apply changes ....'
        val=os.popen('shutdown -r').read()
        print val
