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
User=os.environ["USERPROFILE"]
with disable_file_system_redirection():
    changedir=os.popen("mkdir "+ User+"\AppData\Local\Temp\Low").read()
    create=os.popen("icacls "+ User+"\AppData\Local\Temp\Low /setintegritylevel low").read()
	print create
    print "Now Internet explorer blank page issue fixed successfully"
    
