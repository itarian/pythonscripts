import zipfile
import ctypes

src_path=r'C:\Users\rose\Desktop\files.zip'
dest_path=r'c:\Users'

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
		with zipfile.ZipFile(src_path,"r") as zip_ref:
			zip_ref.extractall(dest_path)
			print 'file unzipped to ' +dest_path 

filezip(src_path,dest_path)
