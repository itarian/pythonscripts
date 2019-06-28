import os
share_path=r'**********'  # Destination share path
share_user="**********"  # share path user name 
share_pass="***********" #share path password
src_path=os.environ['temp']+"\\"+"veeam.zip"  #source folder path need to be copied
import ctypes
import zipfile
path=os.environ['temp']+"\\"+"temp.txt"
zip_path=src_path


class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

def ecmd(command):
    from subprocess import PIPE, Popen
    with disable_file_system_redirection():
        obj = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()
    ret=obj.returncode
    if ret==0:
        if out:
            return out.strip()
        else:
            return "Endpoint has not yet Started backup process. "
    else:
        if err:
            return err.strip()
        else:
            return ret

ps=r''' $A=Get-Eventlog -LogName "Veeam Agent"| where {$_.eventID -eq 190}
$A | Format-List -Property *'''    
with disable_file_system_redirection():
    file_name='powershell_file.ps1'
    file_path=os.path.join(os.environ['TEMP'], file_name)
    with open(file_path, 'wb') as wr:
        wr.write(ps)
        ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
    with open (path,"wb") as f:
        print file_path
        f.write(str(ecmd('powershell "%s"'%file_path)))
        f.close()
def zip_item(path, zip_file_path):  # Creating ZIP file
    print "Zipping up the file\n"
    zip_object=zipfile.ZipFile(zip_file_path, 'w')
    from subprocess import Popen, PIPE, call
    if os.path.isfile(path):
        try:
           os.chmod(path,0644)
        except:
            pass
        zip_object.write(path, path.split(os.sep)[-1])
        zip_object.close()
        return zip_file_path
    else:
        length_directory_path=len(path)
        for root, directories, files in os.walk(path):
            for file_name in files:
                try:
                    os.chmod(file_name,0644)
                except:
                    pass
                file_path=os.path.join(root, file_name) 
                zip_object.write(file_path, file_path[length_directory_path:])
        zip_object.close()
        print "Created Zip_file\n"
        return zip_file_path
def remove():
    try:
        os.remove(path)
        os.remove(zip_path)
        os.remove(src_path)
        os.remove(file_path)
    except:
        pass

zip_item(path,zip_path)
cmd=r'NET USE '+share_path+ r' /USER:'+share_user+'  "'+share_pass+'"'
tar_path=share_path
print 'Login to network share....'
with disable_file_system_redirection():
     print os.popen(cmd).read()

print 'Copying files to network share....'
print os.popen('copy "'+zip_path+'" '+tar_path).read()

remove()
