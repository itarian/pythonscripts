import os
import ctypes
import sys


class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

def alert(arg): 
	sys.stderr.write("%d%d%d" % (arg, arg, arg)) 

with disable_file_system_redirection():
        cmd0="Wevtutil qe Microsoft-Windows-Backup /c:1 /rd:true /f:text"
        run_check_backup = os.popen(cmd0).read()
        run_check_backup = run_check_backup.lower()
def check(run_check_backup):
    for i in [i.strip() for i in run_check_backup.split('\n')  if i.strip()]:
        i = i.lower()
        try:
            if 'backup' in i and 'failed' in i:
                alert(1)
                print 'The Backup event failed'
            elif 'backup' in i and 'cancelled' in i:
                alert(1)
                print 'The Backup event cancelled'
                return i
            elif 'backup' in i and 'failing' in i:
                alert(1)
                print 'The Backup event failing'
                return i
            elif "backup completed successfully":
                alert(1)
                print 'backup completed successfully'
                return i
        except Exception as error:
           pass
a=check(run_check_backup)
if a == None:
    print "There are no successful or failure"
    alert(0)    
