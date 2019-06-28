ps_content=r'''
#Import-Module ServerManager
Import-Module ServerManager
#Install/Enable SNMP Services
Add-WindowsFeature SNMP-Services | Out-Null
netsh advfirewall firewall set rule group="Windows Remote Management" new enable=yes
 
'''
file_name='snmp.ps1' # define your own file name
import os
import subprocess
import sys


def ecmd(command):
    import ctypes
    from subprocess import PIPE, Popen
    
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
        obj = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()
    ret=obj.returncode
    if ret==0:
        if out:
            return out.strip()
        else:
            return ret
    else:
        if err:
            return err.strip()
        else:
            return ret
def verify():
    ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
    out=ecmd('powershell Get-Service | find "SNMP Service"')
    out=str(out)
    if "Running" in out:
        return "SNMP is installed"
    else:
        return "SNMP Not Installed,Plaese restart the system  and try again"
file_path=os.path.join(os.environ['TEMP'], file_name)
with open(file_path, 'wb') as wr:
    wr.write(ps_content)
    wr.close()
    
ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
out=ecmd('powershell Get-Service | find "SNMP Service"')
out=str(out)
if "Running" in out:
	print "SNMP already installed"
else:
    print "Installing SNMP"
    print ecmd('powershell "%s"'%file_path)
    
    ki=verify()
    print ki

    

