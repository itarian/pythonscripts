import os
import socket
from subprocess import Popen, PIPE
import re
import time
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



hostname = socket.gethostname()   
IP = socket.gethostbyname(hostname)


CMD="quser /server:%s" %IP
with disable_file_system_redirection():
    process = Popen(CMD, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
p,e=stdout,stderr

p=re.findall(r"\r\n(.*)",p)
k1=' '.join(p[0].split())
k1=re.findall("rdp-tcp\W[0-9]",k1)


CMD1="reset session %s /server:%s" %(k1[0],IP)
print "Resetting the RDP Session is completed successfully"
time.sleep(10)

with disable_file_system_redirection():
    process = Popen(CMD1, stdout=PIPE, stderr=PIPE)
stdout1, stderr1 = process.communicate()




