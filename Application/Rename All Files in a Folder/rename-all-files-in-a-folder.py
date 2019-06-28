path = itsm.getParameter('Enter_the_path')  ## Enter the path of the folder
Newname=itsm.getParameter('Enter_the_filename') ## Enter the New Name
import os
import ctypes
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

    files = os.listdir(path)
i=1
for file in files:
   format = file.split("\\")[-1]
   os.rename(os.path.join(path, file), os.path.join(path, Newname+str(i)+ format))
   i=i+1
print "All files are renamed successfully"
