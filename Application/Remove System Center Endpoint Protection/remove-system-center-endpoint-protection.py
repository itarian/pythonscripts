def ecmd(cmd, r=False):
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
    from subprocess import PIPE, Popen
    with disable_file_system_redirection():
        OBJ = Popen(cmd, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = OBJ.communicate()
    ret=OBJ.returncode
    if r:
        if ret==0:
            return out.strip()
        else:
            return err.strip()
    else:
        return ret

print ecmd('C:\Windows\ccmsetup\scepinstall.exe /u /s', True)