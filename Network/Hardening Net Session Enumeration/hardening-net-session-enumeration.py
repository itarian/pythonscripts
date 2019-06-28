Revert="YES"

Revert=Revert.upper()
ps_content=r'''

param([switch]$Revert)

function IsAdministrator
{
    param()
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    (New-Object Security.Principal.WindowsPrincipal($currentUser)).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)   
}

function BackupRegistryValue
{
    param([string]$key, [string]$name)
    $backup = $name+'Backup'
    
    #Backup original Key value if needed
    $regKey = Get-Item -Path $key 
    $backupValue = $regKey.GetValue($backup, $null)
    $originalValue = $regKey.GetValue($name, $null)
    
    if (($backupValue -eq $null) -and ($originalValue -ne $null))
    {
        Set-ItemProperty -Path $key -Name $backup -Value $originalValue
    }

    return $originalValue
}

function RevertChanges
{
    param([string]$key,[string]$name)
    $backup = $name+'Backup'
    $regKey = Get-Item -Path $key

    #Backup original Key value if needed
    $backupValue = $regKey.GetValue($backup, $null)
    
    Write-Host "Reverting changes..."
    if ($backupValue -eq $null)
    {
        #Delete the value when no backed up value is found
        Write-Host "Backup value is missing. cannot revert changes"
    }
    elseif ($backupValue -ne $null)
    {
        Write-Verbose "Backup value: $backupValue"
        Set-ItemProperty -Path $key -Name $name -Value $backupValue
        Remove-ItemProperty -Path $key -Name $backup
    } 
      
    Write-Host "Revert completed"
}

if (-not (IsAdministrator))
{
    Write-Host "This script requires administrative rights, please run as administrator."
    exit
}

#NetSessionEnum SecurityDescriptor Registry Key 
$key = "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\DefaultSecurity"
$name = "SrvsvcSessionInfo"
$SRVSVC_SESSION_USER_INFO_GET = 0x00000001

if ($Revert)
{
    RevertChanges -key $key -name $name
    Write-Host "In order for the reverting to take effect, please restart the Server service"
    exit
}

#Backup original Key value if needed
$srvSvcSessionInfo = BackupRegistryValue -key $key -name $name

#Load the SecurityDescriptor
$csd = New-Object -TypeName System.Security.AccessControl.CommonSecurityDescriptor -ArgumentList $true,$false, $srvSvcSessionInfo,0

#Remove Authenticated Users Sid permission entry from its DiscretionaryAcl (DACL)
$authUsers = [System.Security.Principal.WellKnownSidType]::AuthenticatedUserSid
$authUsersSid = New-Object -TypeName System.Security.Principal.SecurityIdentifier -ArgumentList $authUsers, $null
$csd.DiscretionaryAcl.RemoveAccessSpecific([System.Security.AccessControl.AccessControlType]::Allow, $authUsersSid,$SRVSVC_SESSION_USER_INFO_GET, 0,0) 

#Add Access Control Entry permission for Interactive Logon Sid
$wkt = [System.Security.Principal.WellKnownSidType]::InteractiveSid
$interactiveUsers = New-Object -TypeName System.Security.Principal.SecurityIdentifier -ArgumentList $wkt, $null
$csd.DiscretionaryAcl.AddAccess([System.Security.AccessControl.AccessControlType]::Allow, $interactiveUsers, $SRVSVC_SESSION_USER_INFO_GET,0,0)

#Add Access Control Entry permission for Service Logon Sid
$wkt = [System.Security.Principal.WellKnownSidType]::ServiceSid
$serviceLogins = New-Object -TypeName System.Security.Principal.SecurityIdentifier -ArgumentList $wkt, $null
$csd.DiscretionaryAcl.AddAccess([System.Security.AccessControl.AccessControlType]::Allow, $serviceLogins, $SRVSVC_SESSION_USER_INFO_GET,0,0)

#Add Access Control Entry permission for Batch Logon Sid
$wkt = [System.Security.Principal.WellKnownSidType]::BatchSid
$BatchLogins = New-Object -TypeName System.Security.Principal.SecurityIdentifier -ArgumentList $wkt, $null
$csd.DiscretionaryAcl.AddAccess([System.Security.AccessControl.AccessControlType]::Allow, $BatchLogins, $SRVSVC_SESSION_USER_INFO_GET,0,0)

#Update the SecurityDescriptor in the Registry with the updated DACL
$data = New-Object -TypeName System.Byte[] -ArgumentList $csd.BinaryLength
$csd.GetBinaryForm($data,0)
Set-ItemProperty -Path $key -Name $name -Value $data
Write-Host "Permissions successfully updated"
Write-Host "In order for the hardening to take effect, please restart the Server service"

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
if Revert=="YES":
    print ecmd('powershell "%s" -revert'%file_path)
else:
    print ecmd('powershell "%s"'%file_path)
    

os.remove(file_path)
