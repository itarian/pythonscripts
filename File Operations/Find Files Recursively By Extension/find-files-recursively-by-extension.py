recPath='C:\Users\sam\Desktop'## Here mention the path to find files
Ext= '.exe'## here mention extension of the file to find 
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
    def findFilesByExtensionRecursively(recPath, Ext):
        import os
        ls = []
        if os.path.exists(recPath):
            for root, dirs, files in os.walk(recPath):
                for fname in files:
                    if fname.endswith(Ext):
                        ls.append(fname)
            return ls
        else:
            return 'Please provide valid path!'

    if __name__ == '__main__':
        c = 0
        print 'File Name: '
        for i in findFilesByExtensionRecursively(recPath,Ext):
            print i
            c += 1
        print '\n'
        print 'Number of Files: ',c
