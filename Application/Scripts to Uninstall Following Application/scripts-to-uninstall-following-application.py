import subprocess
import os
import ctypes
import re

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
            
system=os.environ["SYSTEMDRIVE"]
CMD=system+r'"\ProgramData\Package Cache\{3d388c41-87ca-4c61-820e-7022cdf762da}\ControlCenterInstaller.exe" /uninstall /quiet'


with disable_file_system_redirection():
    system=os.environ["SYSTEMDRIVE"]
    if os.path.isfile(r'%s\ProgramData\Package Cache\{3d388c41-87ca-4c61-820e-7022cdf762da}\ControlCenterInstaller.exe'%system):
     ping = subprocess.Popen(CMD,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
     print 'uninstall started ConnectWise Control Center'
     out=ping.communicate()[0]
     output = str(out)
     print output
     print 'successfully uninstalled ConnectWise Control Center'
    else:
        print'ConnectWise Control Center not installed on your endpoint'



with disable_file_system_redirection():
    CMD=os.popen('wmic product where name="ScreenConnect" call uninstall').read()
    
if 'ReturnValue = 0' in CMD:
 print 'successfully uninstalled ScreenConnect '
else:
    print'ScreenConnect is not installed on your endpoint'



def check():
    
     with disable_file_system_redirection():
         inst=os.popen("wmic product get name,identifyingnumber").read()
         
        
     return inst
        
def uninstall (find):
	command="MsiExec.exe /X"+find+" /qn CESMCONTEXT=1 REBOOT=REALLYSUPPRESS"
	uninst=os.popen(command).read()
	inst=check()
	find=re.findall('{.*}\s\sESET\sEndpoint\sSecurity',inst)
	if len(find) >0:
		print "ESET Endpoint Security is not uninstalled on Endpoint"
		print "Please restart the computer and Try again"
	else :
		print "Uninstallation is Successful"
inst=check()
 
if len(inst)>0:
	find=re.findall('{.*}\s\sESET\sEndpoint\sSecurity',inst)
	if len(find)>0:
		final=re.findall('{.*}',find[0])[0]
		if len(final) >0:
			print "ESET Endpoint Security   is installed on Endpoint"
			print "Uninstalling has started "
			uninstall(final)
find=re.findall('{.*}\s\sESET\sEndpoint\sSecurity',inst)
if len(find)==0:
    print "ESET Endpoint Security is not installed at End point"












