path='C:\Users\Meteor\Desktop'
Ext ='.txt'
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
    def findFilesByExtension(Path, Ext):
        
        ls = []
        if os.path.exists(Path):
            for fname in os.listdir(Path):
                if fname.endswith(Ext):
                    ls.append(fname)
            return ls
        else:
            return 'Please provide valid path!'

    if __name__ == '__main__':
        c = 0
        print 'File Name: '
        for i in findFilesByExtension(Path,Ext):
            print i
            c += 1
        print '\n'
        print 'Number of Files: ',c
