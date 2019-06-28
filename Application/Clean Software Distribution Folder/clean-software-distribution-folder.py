import os
import subprocess
import ctypes
import shutil

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
    print"Force Detection of Updates and Report will send to the WSUS Server:"
    cmd1="wuauclt.exe /detectnow /reportnow"
    execute=os.popen(cmd1).read()
    print execute
    log=os.environ['SYSTEMROOT']
    log1=log+r'\WindowsUpdate.log'
    log2=os.environ['PROGRAMDATA']
    log3=log2+r'\windowsupdate'
    print "Listing windows Update log details"

    if os.path.isdir(log):
        try:
            shutil.copy2(log1, log2)
            print("%s is copied to %s"%(log1, log2))
            print 'File is successfully copied in Program Data.Please check the logs for the windows update folder in detail'
        except Exception as err :
            print err

    else:
        print 'retry again'

    stop_service="net stop wuauserv"
    service_1=os.popen(stop_service).read()
    print service_1
    stop_bits="net stop bits"
    stop_service=os.popen(stop_bits).read()
    print stop_service
    print"clearing files from software distribution"
    cmd2="del c:\windows\SoftwareDistribution /q /s"
    clear_starts=os.popen(cmd2).read()
    print clear_starts
    print "Cleared the contents from software distribution"
    start_service="net start wuauserv"
    service_2=os.popen(start_service).read()
    print service_2
    start_bits="net start bits"
    start_bits2=os.popen(start_bits).read()
    print start_bits2
    





