## to set disk quota limits per user
drName = 'C:' ## Here you can modify your drive name if you want to set drive 'E:'
threshold = '8000000000' ## warning level in bytes - 8GB set for warning
limit = '10000000000' ## limit level in bytes - 10GB set for limit
username = 'newuser' ## username of the specific user
mode = 'track' ## mode has 2 options - track / enforce; when we use track - disk limit can be crossed by the user but we notified when we use enforce user is blocked to cross his limit

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
    _obj = Popen('fsutil quota {} {}'.format(mode, drName), stdout=PIPE, stderr=PIPE, shell=True)
result = _obj.communicate()
rcode = _obj.returncode
if rcode == 0:
    with disable_file_system_redirection():
        obj = Popen('fsutil quota modify {} {} {} {}'.format(drName, threshold, limit, username), stdout=PIPE, stderr=PIPE, shell=True)
    re = obj.communicate()
    rec = obj.returncode
    if rec == 0:
        print 'disk quota is set for the user {} successfully.\nusage limit: {}\nthreshold level: {}'.format(username, limit, threshold)
    else:
        for ln in re:
            if ln != '':
                print ln
else:
    for line in result:
        if line != '':
            print line
