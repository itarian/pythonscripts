import os
import ctypes
import re
import time
import sys
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


ps_content=r'''

Get-CimInstance -Namespace root/cis AvProfile -Filter "Name = 'Full Scan'" | Invoke-CimMethod -MethodName StartScan
'''
a=0

def ecmd(command):
    import ctypes
    from subprocess import PIPE, Popen

    with disable_file_system_redirection():
        obj = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()
    ret=obj.returncode
    if ret==0:
        if out:
            return out.strip()
        else:
            return ret
    else:
        if err:
            return err.strip()
        else:
            return ret

file_name='powershell_file.ps1'
file_path=os.path.join(os.environ['TEMP'], file_name)
with open(file_path, 'wb') as wr:
    wr.write(ps_content)

def check():
    with disable_file_system_redirection():
        inst=os.popen("wmic product get name,identifyingnumber").read()
         
    return inst
        

inst=check()
 
if len(inst)>0:
    find=re.findall('{.*}\s\sCOMODO\sClient\s-\sSecurity',inst)
    if len(find)>0:
        final=re.findall('{.*}',find[0])[0]
        if len(final) >0:
            a=1

			
if a ==1:
    print ("COMODO Client Security  is installed on Endpoint")
    ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
    print ecmd('powershell "%s"'%file_path)
    print "Successfully started the Full scan in CCS..."
    os.remove(file_path)
        
    
else:
    print ("Comodo Client Security is not installed at End point")

