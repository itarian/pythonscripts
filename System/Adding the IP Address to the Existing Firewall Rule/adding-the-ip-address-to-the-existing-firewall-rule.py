Profile_name='"Network Discovery (LLMNR-UDP-Out)"'#Provide the Existing Firewall Rule Name which you need to add the External ip
myip='8.8.8.8' #Provide the ip which you need to provide
import os
import ssl
import subprocess

ps_content=r'''

Get-NetFirewallRule -displayName %s | Set-NetFirewallRule -RemoteAddress %s

'''%(Profile_name,myip)

import os

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

file_name='powershell_file.ps1'
file_path=os.path.join(os.environ['TEMP'], file_name)
with open(file_path, 'wb') as wr:
    wr.write(ps_content)

ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
val=ecmd('powershell "%s"'%file_path)
if val == 0:
    print "Value has been changed successfully"
os.remove(file_path)

