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
    import os
    uPath = 'C:\\Users'
    lDirectories = os.listdir(uPath)
    dPaths = []
    for eDir in lDirectories:
        uNPath = os.path.join(uPath, eDir)
        try:
            lSDs = os.listdir(uNPath)
            for eSD in lSDs:
                if eSD.lower() == 'downloads':
                    dPaths.append(os.path.join(uNPath, eSD))
                else:
                    continue
        except Exception:
            pass
     
    for dPath in dPaths:
        try:
            os.popen('FOR /D %p IN ("'+dPath+'\\*.*") DO rd "%p" /s /q').read()
            os.popen('del "'+dPath+'\\*" /F /Q').read()
            print(os.popen('dir "'+dPath+'"').read())
        except Exception:
            pass

