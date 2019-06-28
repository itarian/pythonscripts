Username ='111'
Password='111'
remote_pc_ip='11.111.11.111'
ps_cmd='Start-Service ITSMService'

ps_content=r'''
$Username = '%s'
$Password = '%s'
$remote_pc_ip='%s'
$pass = ConvertTo-SecureString -AsPlainText $Password -Force
$SecureString = $pass
# Users you password securly
$MySecureCreds = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $Username,$SecureString 
Invoke-Command -ComputerName $remote_pc_ip -ScriptBlock {%s} -Credential $MySecureCreds'''%(Username,Password,remote_pc_ip,ps_cmd)
file_name='start_itsm.ps1'

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

file_path=os.path.join(os.environ['TEMP'], file_name)
with open(file_path, 'wb') as wr:
    wr.write(ps_content)

ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
print ecmd('powershell  powershell -executionpolicy bypass -File   "%s"'%file_path)
os.remove(file_path)
