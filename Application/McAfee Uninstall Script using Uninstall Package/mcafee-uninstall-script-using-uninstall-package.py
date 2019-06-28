src_path=r'C:\Users\abc\Desktop\McAfee Uninstall.zip'## provide the specific path where the uninstall package resides.
import zipfile
import ctypes
import os
import subprocess
from subprocess import PIPE, Popen
import re
dest_path=os.environ['PROGRAMDATA']
class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
                
def filezip(src_path,dest_path):
   with disable_file_system_redirection():
        Zip_file_1=''
        if src_path.endswith(".zip"):
           with zipfile.ZipFile(src_path,"r") as zip_ref:
               zip_ref.extractall(dest_path)
               Zip_file_1=dest_path+r"\\"+"McAfee Uninstall"
               
        elif src_path.endswith(".exe"):
               Zipee=re.findall("(.*)\MFERemoval100.exe",src_path)[0]
               Zip_file_1=Zipee
                      
        else:
           for dirpath, dirnames, files in os.walk(src_path):
               names=os.listdir(dirpath)
               for i in names:
                   if i == 'MFERemoval100.exe':    
                       Zip_file_1=src_path
        return Zip_file_1                                  
command = "MFERemoval100.exe /MA /noreboot /q"
 
Zip_file=filezip(src_path,dest_path)


def check():
        os.chdir(Zip_file)
        obj = subprocess.Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
        result = obj.communicate()[0]
        print "McAfee Uninstalled successfully"
check()
