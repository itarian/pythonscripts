# '$days=-3' Enter your Preferred value to print the logs in the below script.(For Ex: -3 will print last three days log)

ps_content=r'''
$days=-3
$PrintJobs = Get-WinEvent -FilterHashtable @{Logname = "Microsoft-Windows-TerminalServices-RemoteConnectionManager/Operational" ;ID = 1149,1148,1150;StartTime=(((Get-Date).addDays($days)).date)} -ErrorAction SilentlyContinue
$PrintLogs = @()
    

foreach ($PrintJob in $PrintJobs)
{
  $PrintLog = New-Object -TypeName PSObject -Property @{
    ConnectedMachineLoginUser = $PrintJob.Properties[0].Value
	DomainOrHostname = $PrintJob.Properties[1].Value
    ConnectedIPAddress = $PrintJob.Properties[2].Value
    ConnectionTime = $PrintJob.TimeCreated
    }
  $PrintLogs = $PrintLogs+$PrintLog
  echo $PrintLogs 
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

print "Generating the Endpoint's Remote connection Report ..............."

ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
print ecmd('powershell "%s"'%file_path)


os.remove(file_path)
