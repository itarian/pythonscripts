server_user_name=r"administrator" #provide the username of the server
server_password=r"comodo@123" #provide the password of the server
ps_content=r''' 

[System.Net.Dns]::GetHostbyAddress("10.108.57.56").hostname    #provide the ip address of the server

'''
import subprocess
import ctypes
import getpass
import os
des=os.environ['USERPROFILE']+"\\"+'desktop'
path=os.environ['PROGRAMDATA']+"\\"+'temp'
username=getpass.getuser()
src_path=r'C:'
path= src_path+'\\'+username

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
hostname = ecmd('powershell "%s"'%file_path)
os.remove(file_path)



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
    process=subprocess.Popen('NET USE '+'\\\\'+hostname+'\\C$'+' /u:'+server_user_name+' '+server_password, shell=True, stdout=subprocess.PIPE)
    print process
result=process.communicate()
ret=process.returncode
if ret==0:
    if result[0]:
        print result[0].strip()
    else:
        print None
        
else:
    print '%s\n%s'%(str(ret), str(result[1]))
    
oldpath=path+"\\"+'old.txt'




with disable_file_system_redirection():
    process=subprocess.Popen('ROBOCOPY C:\users'+'\\'+username+'\\'+'Desktop'+" \\\\"+hostname+'\\C$'+'\\'+username+'\\desktop /NP /TEE /E /dcopy:T /Z', shell=True, stdout=subprocess.PIPE)
    print process
    print "The desktop contents are successfully copied to the server"
    print "Please check the path " +path +" in the server " +hostname
result=process.communicate()
ret=process.returncode
if ret==0:
    if result[0]:
        print "success"
    else:
        pass
    
else:
    print '%s\n%s'%(str(ret), str(result[1]))    


    
