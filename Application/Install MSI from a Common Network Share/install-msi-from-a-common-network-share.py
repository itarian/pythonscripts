Folderpath=r'\\Win-u9sfe73clm5\e' #Provide the network share file path
filename=r'ZoomInstallerFull.msi'#provide filename with extension
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
def login(Filepath):    
    
    if not os.path.exists(workdir):
        os.mkdir(workdir)
    with disable_file_system_redirection():        
        
        shutil.copy2(Filepath,workdir)
        print ""+filename+" successfully copied"
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


login(Filepath)

def remove(workdir):
    shutil.rmtree(workdir)

remove(workdir)
