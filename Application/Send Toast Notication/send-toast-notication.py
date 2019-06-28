#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('parameterName') with that parameter's name

TitleText = itsm.getParameter('TitleText')
MessageText = itsm.getParameter('MessageText')
Icon = itsm.getParameter('Icon')
Timeout = itsm.getParameter('Timeout')

ps_content=r'''

Add-Type -AssemblyName System.Windows.Forms 

$TitleText = "%s"
$MessageText = "%s"
$Icon = "%s"
$Timeout = "%s"


$global:balloon = New-Object System.Windows.Forms.NotifyIcon
$path = (Get-Process -id $pid).Path
$balloon.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($path) 
$balloon.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::$Icon
$balloon.BalloonTipText = "$MessageText"
$balloon.BalloonTipTitle = "$TitleText" 
$balloon.Visible = $true 
$balloon.ShowBalloonTip($Timeout)

[Environment]::Exit(0)

'''%(TitleText,MessageText,Icon,Timeout)

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

file_name='toast_notification.ps1'
file_path=os.path.join(os.environ['TEMP'], file_name)
with open(file_path, 'wb') as wr:
    wr.write(ps_content)

ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
print ecmd('powershell "%s"'%file_path)

os.remove(file_path)
