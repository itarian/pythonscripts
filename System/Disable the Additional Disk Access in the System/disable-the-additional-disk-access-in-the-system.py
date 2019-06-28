dl=['?','c'] #mentioned the drives you need Disable the access eg.dl=['e','c']
import _winreg
import platform
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
l=[]
a=[]
l= platform.platform()

if l[9]=='0':
    k=l[:10]

else:
    k=l[:9]
f=[]

for i in dl:
    f.append(i.upper())

key=[]
v=0
drives={'A': '1', 'B': '2', 'C':'4', 'D': '8', 'E': '16','F': '32', 'G':'64', 'H': '128', 'I': '256', 'J': '512', 'K':'1024', 'L': '2048', 'M': '4096', 'N': '8192', 'O': '16384', 'P': '32768', 'Q': '65536', 'R': '131072', 'S': '262144', 'T': '524288', 'U': '1048576', 'V': '2097152', 'W': '4194304', 'X': '8388608', 'Y': '16777216', 'Z': '33554432', 'ALL': '67108863'}

for i in f:
    key.append(drives['%s'%i])
for i in key:
    v=v+int(i)





if k=="Windows-7":
    a=platform.machine()
    if a[3:]=='64':
        s=a[3:]
        k=k+s

if f!=0:
    if(k=="Windows-7"):
        handle = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",0,_winreg.KEY_ALL_ACCESS)
        _winreg.SetValueEx(handle, "NoViewOnDrive", 0, _winreg.REG_DWORD,v)
        print "The Following mentioned drive will be secured"
        for i in f:
            print 'Drive '+'\''+i+':'+'\''+" is Secured"
        print 'Restarting the endpoint to apply changes ....'
        val=os.popen('shutdown -r -t 0').read()
    else:
        handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer",0,_winreg.KEY_ALL_ACCESS)
        _winreg.SetValueEx(handle, "NoViewOnDrive", 0, _winreg.REG_DWORD,v)
        print "The Following mentioned drive will be secured"
        for i in f:
             print 'Drive '+'\''+i+':'+'\''+" is Secured"
        print 'Restarting the endpoint to apply changes ....'
        val=os.popen('shutdown -r -t 0').read()

else:
        handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer",0,_winreg.KEY_ALL_ACCESS)
        _winreg.SetValueEx(handle, "NoViewOnDrive", 0, _winreg.REG_DWORD,0)
        print "All the drive will not be secured in the system"
        print 'Restarting the endpoint to apply changes ....'
        val=os.popen('shutdown -r -t 0').read()
