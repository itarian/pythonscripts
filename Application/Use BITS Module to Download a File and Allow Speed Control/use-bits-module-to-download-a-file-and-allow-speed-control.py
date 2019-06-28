value="2000"  # Give the value of control speed. NOTE: It's in kbps.
path="C:\ProgramData" # Give the path where want to save the downloaded file.

def Registry_change():
    script=r"""
               Const HKEY_LOCAL_MACHINE = &H80000002
    strComputer = "."
    Set oReg=GetObject("winmgmts:{impersonationLevel=impersonate}!\\" & _
    strComputer & "\root\default:StdRegProv")

    strKeyPath = "SOFTWARE\Policies\Microsoft\Windows\BITS"
    oReg.CreateKey HKEY_LOCAL_MACHINE,strKeyPath
    strValueName1 = "EnableBITSMaxBandwidth"
    strValueName2 = "MaxBandwidthValidFrom"
    strValueName3 = "MaxBandwidthValidTo"
    strValueName4 = "MaxTransferRateOffSchedule"
    strValueName5 = "MaxTransferRateOnSchedule"
    strValueName6 = "UseSystemMaximum"
    'Enabled
    dwValue1 = 1
    dwValue2 = 8
    dwValue3 = 17
    dwValue4 = %s
    dwValue5 = 10
    dwValue6 = 1
    oReg.SetDWORDValue HKEY_LOCAL_MACHINE,strKeyPath,strValueName1,dwValue1
    oReg.SetDWORDValue HKEY_LOCAL_MACHINE,strKeyPath,strValueName2,dwValue2
    oReg.SetDWORDValue HKEY_LOCAL_MACHINE,strKeyPath,strValueName3,dwValue3
    oReg.SetDWORDValue HKEY_LOCAL_MACHINE,strKeyPath,strValueName4,dwValue4
    oReg.SetDWORDValue HKEY_LOCAL_MACHINE,strKeyPath,strValueName5,dwValue5
    oReg.SetDWORDValue HKEY_LOCAL_MACHINE,strKeyPath,strValueName6,dwValue6
    
        }"""%(value)

    import ctypes
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
            import os
            path =os.environ['TEMP']
            file = path+'\\'+'Registry_change.vbs'
            fobj= open(file, "w");
            fwrite=fobj.write(script);
            fobj.close();
            run=os.popen('cscript.exe '+file).read();
            print 'Enabled BITS background transfering Process , Speed is Limited with Specified Value.\n'
            print 'Download Started to the Specified path\n'
            try:
                os.remove(file)
            except OSError:
                pass
    return

Registry_change()
percentage="%"
ps_content=r'''
Import-Module BitsTransfer
$file ="http://ftp.belnet.be/mirror/videolan/vlc/2.2.6/win32/vlc-2.2.6-win32.exe"
$path="%s"
$bitsjob = Start-BitsTransfer -Source $file -Destination $path -Asynchronous
while( ($bitsjob.JobState.ToString() -eq 'Transferring') -or ($bitsjob.JobState.ToString() -eq 'Connecting') )
{
$Proc = ($bitsjob.BytesTransferred / $bitsjob.BytesTotal) * 100
}
Get-BitsTransfer
Get-BitsTransfer | Complete-BitsTransfer

Write-Host "Download Completed `n";

Write-Host "Job Details : `n";
'''%(path)

file_name='bits.ps1' # define your own file name

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
print ecmd('powershell "%s"'%file_path)

