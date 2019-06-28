ps_content=r'''
function getstatusvista
{
$EnableLUA =(Get-ItemProperty -Path HKLM:SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System).EnableLUA
if($EnableLUA -eq  0)
{
Write-Host "UAC is disabled"
Set-ItemProperty -Path HKLM:SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System -Name EnableLUA -Value 1 -Type DWord
Write-Host "Enabling UAC ......Settings will be effective after restart"
}
else
{
Write-Host "UAC is Enabled"
Set-ItemProperty -Path HKLM:SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System -Name EnableLUA -Value 0 -Type DWord
Write-Host "Disabling the UAC......Settings will be effective after restart"
}
}
getstatusvista
'''

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
print ecmd('powershell "%s"'%file_path)
os.remove(file_path)
os.popen(r"shutdown /r /t 1")
