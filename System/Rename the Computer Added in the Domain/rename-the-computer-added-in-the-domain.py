Domain=itsm.getParameter('DOMAIN_NAME')
UN=itsm.getParameter('DOMAIN_USER_NAME')
PW=itsm.getParameter('PASSWORD_FOR_DOMAIN_USER')
Old_name=itsm.getParameter('OLD_COMPUTER_NAME')
New_name=itsm.getParameter('NEW_COMPUTER_NAME')

import os

Dom_User=os.path.join(Domain, UN)

ps_content=r'''
$Username = "%s"
$Password = "%s" | ConvertTo-SecureString -AsPlainText -Force
$Creds = New-Object System.Management.Automation.PSCredential($Username ,$Password)


Rename-Computer -NewName %s -ComputerName %s -Restart -DomainCredential $Creds -PassThru  -Verbose
''' %(Dom_User, PW, New_name, Old_name)

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

file_name='Rename.ps1'
file_path=os.path.join(os.environ['PROGRAMDATA'], file_name)
with open(file_path, 'wb') as wr:
    wr.write(ps_content)

ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
os.chdir("C:\Windows\System32\WindowsPowerShell\v1.0")
print ecmd('powershell.exe -command "%s"'%file_path)

os.remove(file_path)
