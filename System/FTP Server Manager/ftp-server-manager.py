service_name=r'ftpsvc'
import ctypes
import os
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
    y=os.popen("wmic service "+service_name+" get state").read()
    if "Stopped" in y:
        print 'The service '+service_name+' was already in stopped state'
        print'So starting the '+service_name+ 'service ........'
        x=os.popen('net start '+service_name).read()
        print 'The Service '+service_name+' has been successfully started'
    elif "Paused" in y:
        print 'The service '+service_name+' was already paused state'
        print 'so stop the '+service_name+' service........'
        z=os.popen('net stop '+service_name).read()
        print 'The Service '+service_name+' has been stopped succesfully'
    elif "Running" in y:
        print "The service "+service_name+' was already in running state'
    else:
        print "The Ftp Server not enabled in your machine"
