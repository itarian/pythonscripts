drive="c:" #Provide the drive which you need to enable Restore Access
ps_content=r'''
enable-computerrestore -drive "%s\"
'''%drive

BAT=r'''
Wmic.exe /Namespace:\\root\default Path SystemRestore Call CreateRestorePoint "My Restore point", 100, 12
'''

import os
import subprocess
import ctypes
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
def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))
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
path=os.environ['programdata']+"\Sample.bat"
with open(path,"w") as f:
    f.write(BAT)

with disable_file_system_redirection():
    process=subprocess.Popen('powershell Get-ComputerRestorePoint',shell=True, stdout=subprocess.PIPE)
result=process.communicate()
ret=process.returncode
if ret==0:
    if result[0]:
        alert(0)
        print "\nAlready existing restore points with creation time\n"
        print result[0].strip()
    else:
        alert(1)
        print "\nThere is no restore points are available in this system"
        ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
        print ecmd('powershell "%s"'%file_path)
        process = subprocess.Popen([path],stdout=subprocess.PIPE)
        stdout = process.communicate()[0]
        print "sucessfully created a new system restore point"
        os.remove(path)
        os.remove(file_path)
        
else:
    print '%s\n%s'%(str(ret), str(result[1]))


