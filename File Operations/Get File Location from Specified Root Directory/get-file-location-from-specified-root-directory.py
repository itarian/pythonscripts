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
    def getFileNameandTargetRootDirectory(fileName, rtDir):
        for root, dirs, files in os.walk(rtDir):
            
            for f in files:
                if f.lower() == fileName:
                    print 'Matched File Name: '+f
                    print('Path: '+os.path.join(root, f))
                    print '\n'
    def main():
        getFileNameandTargetRootDirectory('test.txt','c:\\users\\MSD')
    if __name__=='__main__':
        main()
