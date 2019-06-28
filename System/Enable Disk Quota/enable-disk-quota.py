## to enable disk quota for a specific drive
drName = 'C:' ## Here you can modify your drive name if you want to set drive 'E:'
import ctypes
from subprocess import Popen, PIPE
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
    _obj = Popen('fsutil quota track '+drName, stdout=PIPE, stderr=PIPE, shell=True)
result = _obj.communicate()
output, error = result
if output == '' and error == '':
    print 'disk quota has been enabled for drive {} successfully'.format(drName)
else:
    for line in result:
        if line != '':
            print line
