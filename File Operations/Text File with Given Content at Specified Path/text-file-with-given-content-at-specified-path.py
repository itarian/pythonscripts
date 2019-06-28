import os
k= os.environ.get('USERNAME')
print k
path = 'C:\Users\\'+k+'\AppData\Configfile.inc'
## Pass your content here to write there on the file
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

contents = """
Username="Username"
Password="Password"
IP="0.0.0.0"

"""
with disable_file_system_redirection(): 
    try:
        with open(path, 'w') as fiOb:
            fiOb.write(contents)
            print 'Success: File has been written at - '+path
    except:
        print 'Fail: Check your path!!'
