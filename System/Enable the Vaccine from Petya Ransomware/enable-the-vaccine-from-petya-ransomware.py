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
            

files=['perfc','perfc.dll','perfc.dat']

for i in files:
    filename=os.path.join(os.environ['SYSTEMROOT'],i)
    os.chmod(os.environ['SYSTEMROOT'],0644)
    if not os.path.isfile(filename):
        f=open(filename,'w+')        
        f.close()
        with disable_file_system_redirection():
            print os.popen("'attrib +R'" +filename).read()
        print filename+' Created in system root with read permission'
    else:
        print 'file already exists'

        
print 'Required files have been created to Vaccine Petya ransomware'
