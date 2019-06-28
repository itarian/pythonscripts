#The network share file path
Folderpath=itsm.getParameter('Folderpath')
#provide filename with extension
filename=itsm.getParameter('filename')
# Provide the user name for the shared system
share_user=itsm.getParameter('share_user')
# Provide the password for the shared system
share_pass=itsm.getParameter('share_pass')

Filepath=r""+Folderpath+r'\\'+filename
import os
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

workdir=os.environ['PROGRAMDATA']+r'\temp'
def login(cmd,Filepath):    
    
    if not os.path.exists(workdir):
        os.mkdir(workdir)
    with disable_file_system_redirection():        
        print 'Login to network share'
        print os.popen(cmd).read()
        print 'Copying files to local machine....'
        shutil.copy(Filepath,workdir)
        print "copied successfully"
        path=workdir+"\\"+filename
        if os.path.isfile(path):        
            with disable_file_system_redirection():
                process= subprocess.Popen('msiexec /i "%s" /qn'%path, shell=True, stdout=subprocess.PIPE)
            result=process.communicate()
            ret=process.returncode
            if ret==0:
                pass
            else:
                print result[1]
            print ""+filename+" installed successfully"
        else:
            print '%s is not found.'%path

cmd= 'NET USE "'+Folderpath+'" /USER:'+share_user+'  "'+share_pass+'"'
login(cmd,Filepath)

def remove(workdir):
    shutil.rmtree(workdir)

remove(workdir)
