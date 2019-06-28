src_path=r'C:\abcd'  #source folder path need to be copied 
share_path=r'NINJA\water'  # Destination share path
des_fname='share3'   # please provide the name of the folder that does not exist earlier in the give share path
share_user="ninja-pc"  # share path user name 
share_pass="comodo" #share path password

import os
import shutil
import platform
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

os_details = platform.release()


with disable_file_system_redirection():
    if "7" in os_details:
        print"-------STARTING A SERVICE-----"
        start=os.popen("net start VSS").read()
        print start
        chec=os.popen("sc query VSS").read()
        cmd='NET USE "'+share_path+'" /USER:'+share_user+'  "'+share_pass+'"'
        tar_path=share_path+'\\'+des_fname
        print 'Login to network share'
        print os.popen(cmd).read()
        print 'Copying files to local machine....'
    else:
        cmd='NET USE "'+share_path+'" /USER:'+share_user+'  "'+share_pass+'"'
        tar_path=share_path+'\\'+des_fname
        print 'Login to network share'
        print os.popen(cmd).read()
        print 'Copying files to local machine....'
        
if os.path.isdir(src_path):
    shutil.copytree(src_path,tar_path)
    print 'Script execution completed successfully'
else:
    print '%s is not found'%src_path
