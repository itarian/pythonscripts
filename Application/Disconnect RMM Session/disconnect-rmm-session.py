def ecmd(CMD, OUT=False):
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
        OBJ = Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = OBJ.communicate()
    return out.strip()

print ecmd('net stop CLPSLauncherEx')
print ecmd('taskkill /im unit_manager.exe /f')
print ecmd('taskkill /im unit.exe /f')
import os
os.remove("C:\ProgramData\comodo\lps4\lps-ca\configuration.cfg")
print ecmd('net start CLPSLauncherEx')
