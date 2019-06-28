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
    def findFilesBySizeKB(recPath, limit):
        import os
        ls = []
        if os.path.exists(recPath):
            for root, dirs, files in os.walk(recPath):
                for fname in files:
                    fsize = os.path.getsize(os.path.join(root, fname))/1024
                    if fsize >= limit:
                        ls.append(fname+' '+str(fsize)+'KB')
        return ls


    if __name__=='__main__':
        c = 0
        print 'File Name: '
        for i in findFilesBySizeKB('C:\Users\MSD\Downloads', 6000):
            print i
            c += 1
        print '\n'
        print 'Number of Files: ',c
