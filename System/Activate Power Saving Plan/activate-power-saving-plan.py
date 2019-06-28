import ctypes
import  os
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
    out=os.popen('powercfg.exe /setactive a1841308-3541-4fab-bc81-f71556f20b4a').read();
    print "Activated Power Saved Scheme:"
    out1=os.popen('powercfg  -getActiveScheme').read()
    print out1
