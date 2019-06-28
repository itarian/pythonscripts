import os;
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
    stop=os.popen('net stop spooler').read();
    print(stop);
    clear= os.popen( 'del %systemroot%\System32\spool\printers\* /Q ').read();
    print(clear);
    start=os.popen('net start spooler').read();
    print(start)
