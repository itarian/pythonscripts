def ecmd(CMD, OUT=False):
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
    from subprocess import PIPE, Popen
    with disable_file_system_redirection():
        OBJ = Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = OBJ.communicate()
    return out.strip()


def wfile(fp, c):
    import os
    with open(fp, 'w') as f:
        f.write(c)
    if os.path.isfile(fp):
        return fp
    return

import os
import time
import socket
c=r'''Set objSysInfo = CreateObject("Microsoft.Update.SystemInfo")
Wscript.Echo "Reboot required? " & objSysInfo.RebootRequired'''

fp=os.path.join(os.environ['TEMP'], 'RebootRequired.vbs')
file=wfile(fp, c)
vbsout=ecmd('cscript "'+file+'"')
tim=time.strftime('%d/%m/%Y %H:%M')
cn=os.environ['COMPUTERNAME']
ip=socket.gethostbyname(socket.gethostname())
print 'Date and Time:', tim
print 'Machine Info:', cn+' - '+ip
print '-'*40+'\n'
if 'Reboot required? False' in vbsout:
    print 'The endpoint do not require reboot :)'
    print 'The endpoint do not require reboot :)\n'
elif 'Reboot required? True' in vbsout:
    print 'The endpoint require reboot :(.\nSo please reboot as soon as possible\n'
else:
    print vbsout+'\n'

os.remove(file)
