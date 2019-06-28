#Please provide the username and the password

Username ='john'
Password='admin@123'
ps_content=r'''
$Username = '%s'
$Password = '%s'
$pass = ConvertTo-SecureString -AsPlainText $Password -Force
$SecureString = $pass
# Users you password securly
$MySecureCreds = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $Username,$SecureString 
$repair=Test-ComputerSecureChannel -Repair -Credential $MySecureCreds -Verbose
Write-Host $repair

'''%(Username,Password)

file_name='trust_check.ps1'


import os
import sys
import ctypes

def alert(arg): 
	sys.stderr.write("%d%d%d" % (arg, arg, arg))

   

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
    

    

file_path=os.path.join(os.environ['TEMP'], file_name)
with open(file_path, 'wb') as wr:
    wr.write(ps_content)

def check1():
    with disable_file_system_redirection():
        print os.popen('powershell "Set-ExecutionPolicy RemoteSigned"').read()
        check=os.popen('powershell "Test-ComputerSecureChannel"').read()
        return check  
check=check1()
if 'True' in check:
    print 'Trust connection between this system and the domain server is fine'
    os.remove(file_path)
    alert(0)
else:
    print "attempting repair"
    print os.popen('powershell.exe -executionpolicy bypass -File "%s"'%file_path).read()
    print "Repair attempted"
    check=check1()
    if 'True' in check:
        print 'Trust connection between this system and the domain server is working now'
        os.remove(file_path)
        alert(1)
    else:
        print "Unable to repair "
        alert(1)

