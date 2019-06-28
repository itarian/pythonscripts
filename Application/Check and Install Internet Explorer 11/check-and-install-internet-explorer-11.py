#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('variableName') with that parameter's name

import os
import sys
import platform
import subprocess
import ctypes
import _winreg
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

def machine():
    """Return type of machine."""
    if os.name == 'nt' and sys.version_info[:2] < (2,7):
        return os.environ.get("PROCESSOR_ARCHITEW6432", 
               os.environ.get('PROCESSOR_ARCHITECTURE', ''))
    else:
        return platform.machine()

def os_bits(machine=machine()):
    """Return bitness of operating system, or None if unknown."""
    machine2bits = {'AMD64': 64, 'x86_64': 64, 'i386': 32, 'x86': 32}
    return machine2bits.get(machine, None)

x=(os_bits())

registry_key=r'HKEY_LOCAL_MACHINE\Software\Microsoft\Internet Explorer'
try:
    reg_key=registry_key.split(os.sep)
    key = getattr(_winreg,reg_key[0])
    subkey = _winreg.OpenKey(key, os.sep.join(reg_key[1:]), 0, _winreg.KEY_ALL_ACCESS)
    (y, type) = _winreg.QueryValueEx(subkey,"svcversion")
    value=y.split(".")[0]
except:
    reg_key=registry_key.split(os.sep)
    key = getattr(_winreg,reg_key[0])
    subkey = _winreg.OpenKey(key, os.sep.join(reg_key[1:]), 0, _winreg.KEY_ALL_ACCESS)
    (y, type) = _winreg.QueryValueEx(subkey,"version")
    value=y.split(".")[0]
   
def Download(URL):
    import urllib2
    import os
    print "Download started"
    fn = URL.split('/')[-1]
    src_path=os.environ['ProgramData']+'\c1_temp'
    fp = os.path.join(src_path, fn)
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    if os.path.exists(src_path):
        print "Path already exists"
    if not os.path.exists(src_path):
        os.makedirs(src_path)
        print "Path created"
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    return fp

if value=="11":
    print "The Internet Explorer is already updated"
elif x == 32:
    URL='http://download.microsoft.com/download/9/2/F/92FC119C-3BCD-476C-B425-038A39625558/IE11-Windows6.1-x86-en-us.exe'
    fn = URL.split('/')[-1]
    xx=Download(URL)
    silent='/quiet'
    print'Downloaded Application %s Installation Started'%xx
    print "System going to restart after installation"
    y=os.popen(xx+' '+silent).read()
           
else:
    URL='http://download.microsoft.com/download/7/1/7/7179A150-F2D2-4502-9D70-4B59EA148EAA/IE11-Windows6.1-x64-en-us.exe'
    fn = URL.split('/')[-1]
    xx=Download(URL)
    silent='/quiet'
    print'Downloaded Application %s Installation Started'%xx
    print "System going to restart after installation"
    y=os.popen(xx+' '+silent).read()
