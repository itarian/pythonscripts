printer_name=r'Microsoft XPS Document Writer' #provide printer name to set as default

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
    try:
        com=os.popen('wmic printer get name').read()
        if printer_name in com:
            cmd=os.popen('wmic printer where default=true get name').read()   
            if printer_name in cmd:
                print '%s is your default printer already..............' %(printer_name)
            else:
                cmd1=os.popen('RUNDLL32 PRINTUI.DLL,PrintUIEntry /y /n "%s"' %(printer_name)).read()
                print 'Successfully changed your default printer as %s .............' %(printer_name)
        else:
            print 'ERROR - %s printer is not configured or check your printer name' %(printer_name)
    except Exception as err: 
        print "Failed due to the below error"
        print err
