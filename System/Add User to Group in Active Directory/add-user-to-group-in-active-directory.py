group_name="*****" #Edit with your group name
user_name="*****" #Edit with you user name

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

with disable_file_system_redirection():
    cmd=os.popen("net group").read()
    cmd1=os.popen("net user").read()
    if group_name in cmd:
        if user_name in cmd1:
            ps_command='net group "%s" "%s" /ADD /DOMAIN'%(group_name,user_name)
            process=os.popen(ps_command).read()
            if "completed" in process:
                print "User %s added to the group %s"%(user_name,group_name)
            else:
                print "User %s is already a member of group %s"%(user_name,group_name)
        else:
            print "There is no such user: %s"%(user_name)
    else:
        print "There is no such group: %s"%(group_name)
    
    

    



