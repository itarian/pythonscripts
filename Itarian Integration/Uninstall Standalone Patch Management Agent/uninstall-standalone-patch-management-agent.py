import os
import ctypes
import re
import time

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
def check():
    
    with disable_file_system_redirection():
        inst=os.popen("wmic product get name,identifyingnumber").read()
         
        
    return inst
        
def uninstall (find):
    with disable_file_system_redirection():
        command='wmic product where name="Comodo One Patch Management Agent" call uninstall'
        uninst=os.popen(command).read()
        time.sleep(1)
    inst=check()
       
    find=re.findall('{.*}\s\sComodo\sOne\sPatch\sManagement\sAgent',inst)
    if len(find) >0:
        
        print "Comodo One Patch Management Agent is not uninstalled on Endpoint"
        print "Please restart the computer and Try again"
    else :
        print "Uninstallation is Successful"

inst=check()

if len(inst)>0:
    find=re.findall('{.*}\s\sComodo\sOne\sPatch\sManagement\sAgent',inst)
    if len(find)>0:
            final=re.findall('{.*}',find[0])[0]
            if len(final) >0:
                    print "Comodo One Patch Management Agent is installed on Endpoint"
                    print "Uninstalling has started "
                    uninstall(final)
			
find=re.findall('{.*}\s\sComodo\sOne\sPatch\sManagement\sAgent',inst)
if len(find)==0:
	print "Comodo One Patch Management Agent is not installed at End point"
