key=itsm.getParameter('key')
ps_content=r'''

If (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{   
	$arguments = "& '" + $myinvocation.mycommand.definition + "'"
	Start-Process powershell -Verb runAs -ArgumentList $arguments
	Break
}

Function ChangeWindowskey
{
	#Get the key
	$key = "%s"  #### Please enter your product key here
    Write-Host "Try to import key,please wait..."
    $Result1 = Cscript.exe $env:SystemRoot\System32\slmgr.vbs -ipk $key
	$Str1 = $Result1 | Select-Object  -Last 2
	#try to active the product.
    Write-Host "$Str1" -ForegroundColor Green
	Write-Host "Try to active Windows product,please wait."
	$Result2 = Cscript.exe $env:SystemRoot\System32\slmgr.vbs -ato
	$Str2 = $Result2 | Select-Object -Last 2
	Write-Host "$Str2" -ForegroundColor Green		  
}
'''%key

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
