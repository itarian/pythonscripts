service_name=r'xxxxxx'   # Give the exact service name

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

import os
with disable_file_system_redirection():
    print os.popen("sc config "+service_name+" start=auto").read()
    y=os.popen("wmic service "+service_name+" get state").read()
    
    if "Stopped" in y:
        try:            
            print 'The service '+service_name+' was already in stopped state'           
            print 'So starting the '+service_name+ 'service ........'            
            x=os.popen('net start '+service_name).read()            
            print 'The Service '+service_name+' has been successfully started'            
        except Exception as err: 
            print "Unable to start the Service" +service_name+'due to below error'
            print err                                         
    else:
        print "The service "+service_name+' was already in running state'
       
