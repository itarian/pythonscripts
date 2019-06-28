ps_content=r'''

    $computer =  $env:COMPUTERNAME
    $namespace = "ROOT\CIMV2"
    $classname = "Win32_Printer"

    Write-Output "====================================="
    Write-Output "COMPUTER : $computer "
    Write-Output "CLASS    : $classname "
    Write-Output "====================================="

    Get-WmiObject -Class $classname -ComputerName $computer -Namespace $namespace |
        Select-Object * -ExcludeProperty PSComputerName, Scope, Path, Options, ClassPath, Properties, SystemProperties, Qualifiers, Site, Container |
        Format-List -Property [a-z]* 

    Next


'''

import os
import re

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
file_name1='printer.txt'
file_path=os.path.join(os.environ['TEMP']+'\\'+file_name)
file_path1=os.path.join(os.environ['TEMP']+'\\'+file_name1)
with open(file_path, 'wb') as wr:
    wr.write(ps_content)

ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
command= "powershell " + '"'+file_path+'"'+ " " + ">" + " " +'"'+ file_path1+'"'
ecmd(command)

print "************Printer Name = DeviceID || Port Name = PortName || DriverName = DriverName***************"

if  os.path.exists(file_path1):    
    with open (file_path1, 'r') as file:
        for line in file:
            string=''
            line=line.strip()
            if 'DeviceID' in line or 'PortName' in line or 'DriverName' in line:
                if 'PNPDeviceID' in line:
                    pass
                else:
                    if line=='':
                       continue
                    else:
                       line=line.strip()
                       string+=''.join(line)
                    print string

os.remove(file_path)
os.remove(file_path1)
