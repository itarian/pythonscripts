Folderpath=r"\\SHORE-PC\Users\Wave\Desktop\VICKY" #Provide the network share file path
filename=r"taksi-0.7.7.9-dev.msi"                 #Provide filename with extension
share_user="CHANGE ME"                            #Provide the user name for the shared system
share_pass="CHANGE ME"                            #Provide the password for the shared system
import os
Filepath=os.path.join(Folderpath,filename)
print Filepath
import shutil
import ctypes
import subprocess


class disable_file_system_redirection:
 _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
 _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
 def __enter__(self):
     self.old_value = ctypes.c_long()
     self.success = self._disable(ctypes.byref(self.old_value))
 def __exit__(self, type, value, traceback):
     if self.success:
         self._revert(self.old_value)

workdir=os.environ['TEMP']
def login(path, RES = False):
    CMDS='MsiExec.exe /i "'+path+'" /qn /L*v "'+os.path.join(workdir, filename.split('.')[0])+'.log"'
    if not os.path.exists(workdir):
        os.mkdir(workdir)
    with disable_file_system_redirection():
        from subprocess import PIPE, Popen
        OBJ = Popen(CMDS, shell = True, stdout = PIPE, stderr = PIPE)
        out, err = OBJ.communicate()
        RET = OBJ.returncode
    if RET == 0:
        if RES == True:
            if out:
                return out.strip()
            else:
                return True
        else:
            return True
    else:
        if RES == True:
            if err:
                return err.strip()
            else:
                return False
        else:
            return False


def remove(workdir):
 shutil.rmtree(workdir)

def cafee(LocalFilePath,command):
 with disable_file_system_redirection():
     process=subprocess.Popen([LocalFilePath, command],stdout=subprocess.PIPE);
     result=process.communicate()[0]
     print (result)
 


cmd= r'NET USE "'+Folderpath+r'" /USER:'+share_user+' "'+share_pass+'"'
print 'Login to network share'
print os.popen(cmd).read()
print 'Copying files to local machine....'
shutil.copy(Filepath,workdir)
print "copied successfully"
path=workdir+"\\"+filename
login(path, True)
import time
time.sleep(3)
try:
    os.remove(path)
except:
    pass
print 'Success: Installing '+filename+' is Completed'
print 'Check the Log file for more details >> '+os.path.join(workdir, filename.split('.')[0])+'.log"'
