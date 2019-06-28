Drive="D:" ##Enter the Drive you want to decrypt
save="C:" ##Enter the Drive you want to save the recovery key

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
y=[]
xx=[]
k=[]
fp=os.path.join(save+r"\\Recoverykey.txt")
print fp
if "Unlocked" in pro:
    print "Drive "+Drive+" is now in locked state"
    ps_command=r'manage-bde -on '+Drive+' -RecoveryKey '+save+' -RecoveryPassword'
    
    with disable_file_system_redirection():
        c=os.popen('powershell "%s"'%ps_command).read()
        y=c.split('\n')
        
        for i in range(len(y)):
            if re.findall('ACTIONS REQUIRED:(.*)',y[i]):
                j=i
                for yy in y[j:]:
                    k.append(yy)


with open(fp, 'a+') as f:
    for i in k:
        print i
        f.write(str(i))                    
