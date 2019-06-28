ps_content=r'''

$definition = @"
using System;
using System.Runtime.InteropServices; 
 
namespace Win32Api
{
 
    public class NtDll
    {
        [DllImport("ntdll.dll", EntryPoint="RtlAdjustPrivilege")]
        public static extern int RtlAdjustPrivilege(ulong Privilege, bool Enable, bool CurrentThread, ref bool Enabled);
    }
}
"@ 
 
Add-Type -TypeDefinition $definition -PassThru | Out-Null
[Win32Api.NtDll]::RtlAdjustPrivilege(9, $true, $false, [ref]$false) | Out-Null
 
#Setting ownership to Administrators
$key = [Microsoft.Win32.Registry]::LocalMachine.OpenSubKey("SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\DefaultMediaCost",[Microsoft.Win32.RegistryKeyPermissionCheck]::ReadWriteSubTree,[System.Security.AccessControl.RegistryRights]::takeownership)
$acl = $key.GetAccessControl()
$acl.SetOwner([System.Security.Principal.NTAccount]"Administrators")
$key.SetAccessControl($acl)
 
#Giving Administrators full control to the key
$rule = New-Object System.Security.AccessControl.RegistryAccessRule ([System.Security.Principal.NTAccount]"Administrators","FullControl","Allow")
$acl.SetAccessRule($rule)
$key.SetAccessControl($acl)
 
#Setting Ethernet as metered or not metered
$path = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\DefaultMediaCost"
$name = "Ethernet"
$metered = Get-ItemProperty -Path $path | Select-Object -ExpandProperty $name

Clear
if ($metered -eq 1)
{
        New-ItemProperty -Path $path -Name $name -Value "2" -PropertyType DWORD -Force | Out-Null

        Write-Host "Ethernet is now set to metered."
}
elseif ($metered -eq 2)
{
        Write-Host "Ethernet is already set to metered."
}
 
     



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
