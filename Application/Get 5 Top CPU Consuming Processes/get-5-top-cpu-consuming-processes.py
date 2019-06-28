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
    load=os.popen('wmic cpu get loadpercentage /format:list').read();
    print(load);
    print('Top cpu consuming processes \n');
    process=os.popen('tasklist /v /FI "CPUTIME gt 00:03:00" | sort /R /+148').readlines();
    try:
        for i in range(1,7,1):
            print (process[i]);
    except:
        print("Finished");
