Filepath=itsm.getParameter('share_path')                                        ##Provide the network share file path
share_user=itsm.getParameter('share_user')                                            ## Provide the user name for the shared path
share_pass=itsm.getParameter('share_pass')                                              ## Provide the password for the shared path
Setup_Path_X64=itsm.getParameter('share_setup_64')    ## Enter the .msi file name for 64 bit
Setup_Path_X86=itsm.getParameter('share_setup_32')     ##  Enter the .msi file name for 32 bit

import os
import shutil
import ctypes
import subprocess
import socket
import time
from shutil import copyfile


path=r"C:\Program Files (x86)"
if os.path.exists(path):
    NFN=Setup_Path_X64    
else:
    NFN=Setup_Path_X86
    
CP=os.path.join(Filepath,NFN)
workdir=os.environ["TEMP"]
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
            
def login(cmd,Filepath,CP):
    with disable_file_system_redirection():        
        print 'Login to network share'
        print os.popen(cmd).read()
        print 'Copying  file from Network share....'
        print os.popen('copy "'+CP+'" '+workdir).read()
                
cmd= 'NET USE "'+Filepath+'" /USER:'+share_user+'  "'+share_pass+'"'
login(cmd,Filepath,CP)
PTI=os.path.join(workdir,NFN)
CMD ='msiexec /i  "'+PTI+'"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=1 CES_FIREWALL=1 CES_ANTIVIRUS=1  '
os.popen(CMD)

if 'PROGRAMW6432' in os.environ.keys():
    CMD_1='"C:\Program Files (x86)\COMODO\Comodo ITSM\ITSMService.exe" -c 4'

else:
    CMD_1='"C:\Program Files\COMODO\Comodo ITSM\ITSMService.exe" -c 4'

with disable_file_system_redirection():
    ping = subprocess.Popen(CMD_1,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
    out=ping.communicate()[0]
    output = str(out)
    print output

os.remove(PTI)
