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


filepath = os.environ['PROGRAMDATA']
os.chdir(filepath)
if os.path.isdir('C1_TEMP'):
    print " "
else:
    os.mkdir('C1_TEMP')
networkfile = filepath+'\\C1_TEMP\\newtworkfile.txt'

with disable_file_system_redirection():            
    ip_check=os.popen("ipconfig").read()

for ip in [ip.strip() for ip in ip_check.split('\n') if 'IPv4 Address'  in ip if ip.strip()]:
    s=ip
    ip_log=s[36:]
print "Testing the network connetivity for the endpoint with an ip: "+ip_log+"..."

ping="ping "+ip_log



with disable_file_system_redirection():
    check_connectivity=os.popen(ping).read()

for lost in [lost.strip() for lost in check_connectivity.split('\n') if 'Lost'  in lost if lost.strip()]:
    connection_lost = lost[33:]


if os.path.isfile(networkfile):
    with open(networkfile,'r+') as f:
        countinfile = f.read()
else:
    with open(networkfile,'w+') as f:
        f.truncate()
        f.write('0')
    with open(networkfile,'r+') as f:
        countinfile = f.read()

    
if "Lost = 0" in connection_lost:
    if '1' in  countinfile:
        alert(0)
        print "The network connectivity is good"
    elif '2' in  countinfile:
        alert(1)
        print check_connectivity
        with open(networkfile,'w+') as f:
            f.truncate()
            f.write('1')
    else:
        alert(1)
        print check_connectivity
        with open(networkfile,'w+') as f:
            f.truncate()
            f.write('1')
    
elif "Destination host unreachable" or "Request timed out" in check_connectivity:
    if '2' in  countinfile:
        alert(0)
        print "The Destination host is unreachable"
    elif '1' in  countinfile:
        print check_connectivity
        alert(1)
        with open(networkfile,'w+') as f:
            f.truncate()
            f.write('2')
    else:
        print check_connectivity
        alert(1)
        with open(networkfile,'w+') as f:
            f.truncate()
            f.write('2')

