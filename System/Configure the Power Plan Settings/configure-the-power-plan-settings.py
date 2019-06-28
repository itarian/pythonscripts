option='3' # provide option for selecting the operation to perform
#option 1: Enabling Balanced Power scheme
#option 2: Enabling High Performance Power scheme
#option 3: Enabling Power saver Scheme
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

if option=='1':
    print "Enabling Balanced Power Scheme"
    print os.popen('powercfg.exe /setactive 381b4222-f694-41f0-9685-ff5bb260df2e').read()

elif option=='2':
    print "Enabling High Performance Power Scheme"
    print os.popen('powercfg.exe /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c').read()

elif option=='3':
    print "Enabling Power saver Scheme"
    print os.popen('powercfg.exe /setactive a1841308-3541-4fab-bc81-f71556f20b4a').read()

else:
    print "No such option"

out1=os.popen('powercfg  -getActiveScheme').read()
print "Activated Power Saved Scheme:"
print out1
    
