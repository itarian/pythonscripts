Folderpath=r'\\XXX-PC\pic' #Provide the network share file path
filename=r'XXX.jpg'#provide filename with extension
share_user="wave" # Provide the user name for the shared system
share_pass="comodo24" # Provide the password for the shared system
Filepath=r""+Folderpath+r'\\'+filename
import os
import shutil
import ctypes
import subprocess
cmd= 'NET USE "'+Folderpath+'" /USER:'+share_user+' "'+share_pass+'"'
workdir=os.environ['PROGRAMDATA']+r'\temp'
shutil.rmtree(workdir,ignore_errors=True)
if not os.path.exists(workdir):
     os.mkdir(workdir) 
print os.popen(cmd).read()
shutil.copy(Filepath,workdir)
path=workdir+"\\"+filename
ps_content=r'''
$value = "%s"
Set-ItemProperty -path 'HKCU:\Control Panel\Desktop\' -name wallpaper -value $value
rundll32.exe user32.dll, UpdatePerUserSystemParameters
'''%(path)
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
print ecmd('powershell "%s"'%file_path)

print ecmd('shutdown -r -t 00')




