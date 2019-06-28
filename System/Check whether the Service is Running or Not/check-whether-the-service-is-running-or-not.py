serName='power' # pass your service name 
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
    def IsServiceRunning(serName):
        import os
        proObj = os.popen('TASKLIST /svc /FI "Services eq '+serName+'"')
        runServices = proObj.read()
        return runServices
     
    ## pass your service name as a argument in "print IsServiceRunning('arg-service-name')"
    print IsServiceRunning(serName)
