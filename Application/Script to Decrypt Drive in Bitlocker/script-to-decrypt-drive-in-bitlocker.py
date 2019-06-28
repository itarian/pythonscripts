RecoveryKey="405658-268631-257433-019745-265023-067408-284086-217767" ##Enter the Recovery key
Drive="E:" ##Enter the Drive you want to decrypt

import ctypes
import re
import os

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
 
import subprocess
path = 'C:\\Windows\\System32\\manage-bde.exe -status '+Drive
with disable_file_system_redirection():
    process=subprocess.Popen((path),shell=True,stdout=subprocess.PIPE);
result=process.communicate()[0]

protect=re.findall("Lock Status:          (.*)",result)
pro="".join(protect)

if "Locked" in pro:
    print "Drive "+Drive+" is now in locked state"
    ps_command=r'manage-bde -unlock '+Drive+' -rp '+RecoveryKey
    with disable_file_system_redirection():
        process=subprocess.Popen('powershell "%s"'%ps_command, shell=True, stdout=subprocess.PIPE)
    result=process.communicate()
    ret=process.returncode
    if ret==0:
        if result[0]:
            print result[0].strip()
            print "Drive "+Drive+" is now decrypted"
        else:
            print None
        
    else:
        print '%s\n%s'%(str(ret), str(result[1]))
    
else:
    print "Drive "+Drive+" is in unlocked state and is not encrypted"
    
