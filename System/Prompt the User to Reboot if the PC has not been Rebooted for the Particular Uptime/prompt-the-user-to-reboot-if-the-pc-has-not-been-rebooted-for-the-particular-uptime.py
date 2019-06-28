days=8   ##set any number of days that the up time of the system
def ecmd(CMD, OUT=False):
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
    from subprocess import PIPE, Popen
    with disable_file_system_redirection():
        OBJ = Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = OBJ.communicate()
    return out.strip()


def wfile(fp, c):
    import os
    with open(fp, 'w') as f:
        f.write(c)
    if os.path.isfile(fp):
        return fp
    return

import os
import time
import socket
c=r'''Set objSysInfo = CreateObject("Microsoft.Update.SystemInfo")
Wscript.Echo "" & objSysInfo.RebootRequired'''
p=r'''$os = Get-WmiObject win32_operatingsystem
$uptime = (Get-Date) - ($os.ConvertToDateTime($os.lastbootuptime))
$uptime = (Get-Date) - ($os.ConvertToDateTime($os.lastbootuptime))
Write-Output $Uptime.Days'''

fp=os.path.join(os.environ['TEMP'], 'RebootRequired.vbs')
pf=os.path.join(os.environ['TEMP'], 'checkboottime.ps1')
file=wfile(fp, c)
filep=wfile(pf, p)
vbsout=[i.strip() for i in ecmd('cscript "'+file+'"').split('\n') if i.strip()][-1]

##print vbsout
pcmd='PowerShell.exe -ExecutionPolicy Bypass -File %s'%(filep)
psout=ecmd(pcmd)
##print psout

tim=time.strftime('%d/%m/%Y %H:%M')
cn=os.environ['COMPUTERNAME']
ip=socket.gethostbyname(socket.gethostname())
print 'Date and Time:', tim
print 'Machine Info:', cn+' - '+ip
print '-'*40

if vbsout=='True' or psout>=days:
    def alert(input_text):
        c1=r'''MsgBox "%s"'''%(input_text)
        u=r'''Set objNetwork = CreateObject("Wscript.Network")
Wscript.Echo objNetwork.UserName'''
        pm=os.path.join(os.environ['TEMP'], 'messagealert.vbs')
        pu=os.path.join(os.environ['TEMP'], 'finduser.vbs')
        filem=wfile(pm, c1)
        fileu=wfile(pu, u)
        ecmd('cscript "%s"'%filem)
        user=ecmd('cscript "%s"'%fileu)
        print 'The following alert message is sent to the user "%s"'%([i.strip() for i in user.split('\n') if i.strip()][-1])
        print input_text
        os.remove(filem)
        os.remove(fileu)
        return
    if vbsout=='True':
        alert('Please reboot your system! Because the system was not restarted after the Windows Update was complete.')
    elif psout>=days:
        alert('Please reboot your system! Because your system has not had a fresh startup in %s days.'%str(psout))
else:
    print 'No alert is sent to the user. Because, \n\nThe system uptime is only %s days.\nAnd It has no pending restart as well.'%str(psout)

os.remove(file)
os.remove(filep)
