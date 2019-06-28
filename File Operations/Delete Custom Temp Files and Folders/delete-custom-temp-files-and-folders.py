import os
drive = os.environ['SYSTEMDRIVE']
del_dir=[drive+r"\Windows\Logs\CBS\CBS.log",drive+r"\Windows\Temp\ccsetup532.exe",drive+r"\Users\Sample\AppData\Local\Temp\spmlogs"] ## Here mention the paths which you want to delete
import os
import subprocess
import ctypes
import stat
import shutil
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

print 'Deleting temp files begins...  '
for i in del_dir:
    if os.path.exists(i):
       Path = os.path.isdir(r"%s" %(i))
       Path = str(Path) 
       if "False" in Path:
            try:
                print "Deleting File"
                os.chmod(i,0644)
                os.remove(i)
                print "Deleted "+ i
                print "Deleted Successfully"
            except Exception as error:
                print "The file working in another process" + i
       else:
            try:
                print "Deleting Directory"
                os.chmod(i,0644)
                shutil.rmtree(i)
                print "Deleted"+ i
                print "Deleted Successfully"
            except Exception as error:
                print "The Folder working in another process" +i
    else:
         print "Please give the valid path"
                
