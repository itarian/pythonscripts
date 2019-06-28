#option 1: To uninstall the selected default apps in windows 10
#option 2: To restore all the default builin apps in windows 10
option=itsm.getParameter('parameterName') # provide option for selecting the operation to perform
apps =r'windowscalculator' # provide the name of the default apps here
ps_command=r'Get-AppxPackage *%s* | Remove-AppxPackage'%apps
ps_content=r'Get-AppxPackage -AllUsers| Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\AppXManifest.xml"}'
import os
import subprocess
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
def uninstall():
    try:
        with disable_file_system_redirection():
            process=subprocess.Popen('powershell "%s"'%ps_command, shell=True, stdout=subprocess.PIPE)
            result=process.communicate()
            ret=process.returncode
            if ret==0:
                if result[0]:
                    print result[0].strip()                
            else:
                print '%s\n%s'%(str(ret), str(result[1]))
    except:
        process=subprocess.Popen('powershell "%s"'%ps_command, shell=True, stdout=subprocess.PIPE)
        result=process.communicate()
        ret=process.returncode
        if ret==0:
            if result[0]:
                print result[0].strip()
        else:
            print '%s\n%s'%(str(ret), str(result[1]))

def reinstall():
    try:
        with disable_file_system_redirection():
            process=os.popen('powershell.exe "%s"'%ps_content).read()
            
    except:
        process=os.popen('powershell.exe "%s"'%ps_content).read()
        
        
if option == 1:
    print "Uninstalling the %s has started"%apps
    uninstall()
    print "\t*) Uninstalling the %s has been successfully finished"%apps
elif option == 2:
    print "Restore all the default builin apps Started...\n"
    reinstall()
    print "\t*) Restore all the default builin apps has been successfully finished\n"

else:
    print "invalid option"
