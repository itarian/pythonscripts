# The script is a template to check UAC status on device. 
import os 
import sys 
import _winreg 

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg)) 

# Please use "alert(1)" to turn on the monitor(trigger an alert) 
# Please use "alert(0)" to turn off the monitor(disable an alert) 
# Please do not change above block and write your script below 

Drive='C'
ps_command=r'manage-bde -status '+Drive+':' 
import os,re
import subprocess,sys,ctypes
from subprocess import PIPE,Popen

def alert(arg): 
	sys.stderr.write("%d%d%d" % (arg, arg, arg)) 

# Please use "alert(1)" to turn on the monitor(trigger an alert) 
# Please use "alert(0)" to turn off the monitor(disable an alert) 
# Please do not change above block and write your script below



def ressus():
    vbs=r'''
    Set objSysInfo = CreateObject("Microsoft.Update.SystemInfo")
    Wscript.Echo "Reboot required? " & objSysInfo.RebootRequired
    '''
    import os
    import sys
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
    f=0

    def runvbs(vbs):
        workdir=os.environ['PROGRAMDATA']+r'\temp'
        if not os.path.isdir(workdir): 
            os.mkdir(workdir)
        with open(workdir+r'\temprun.vbs',"w") as f :
            f.write(vbs)        
        with disable_file_system_redirection():
            k= os.popen('cscript.exe "'+workdir+r'\temprun.vbs"').read()
            return k
            
            
        if os.path.isfile(workdir+r'\temprun.vbs'):
            os.remove(workdir+r'\temprun.vbs')

    k=runvbs(vbs)
    if 'Reboot required? False' in k:
        ale=0
        print 'The system does not required the reboot and the bitlocker is Resumed...'
        ps_command1=r'Resume-BitLocker -MountPoint "C:"'
        print os.popen('powershell "%s"'%ps_command1).read()
  
    else :
        ale=1
        print 'Rebooot Required in the system and the bitlocker is suspended for the Reboot so please Reboot the system As soon as possible..'
        ps_command2=r'Suspend-BitLocker -MountPoint "C:" -RebootCount 0'
        print os.popen('powershell "%s"'%ps_command2).read()



    if ale > 0:
        alert(1)
    else:
        alert(0)


def checkdrive():
    result=os.popen(ps_command).read()
    m=result.strip()
    n=re.findall('Conversion\sStatus:\s\s\s\s(.*)',m)        
    if "Fully Decrypted" in n:
        print "Bitlocker is not enabled for "+Drive+" Drive"
        alert(0)
    else:
        ressus()


checkdrive()

