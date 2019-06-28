ps_content=r'''
Get-WinEvent -LogName "Microsoft-Windows-Backup" -FilterXPath "*[System[Level=4 and TimeCreated[timediff(@SystemTime) <= 86400000]]]"
'''

import os
import re
import sys
def alert(arg): 
    sys.stderr.write("%d%d%d" % (arg, arg, arg))
	
def ecmd(command):
    import ctypes
    from subprocess import PIPE, Popen
    
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

ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
ar=ecmd('powershell "%s"'%file_path)

if "The backup operation has finished successfully." in ar:
    print ("backup has occurred in past 24 hours")
    alert(1)
else:
    print ("backup has not occurred in past 24 hours")
    alert(0)
    

os.remove(file_path)
