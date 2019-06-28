import os
import shutil
import sys 
import random
import ctypes

def delete_update():
    n=random.randint(10000, 20000)
    p='C:\\Windows\\SoftwareDistribution'
    rn='ren "%s" "%s"'%(p, n)
    pn='C:\\Windows\\%s'%n
    print 'Stopping Windows Update Service %s %s'%('.'*20, ecmd('net stop wuauserv')==0)
    print 'Disabling Windows Update Service %s %s'%('.'*20, ecmd('sc config wuauserv start= disabled')==0)
    print 'Disabling BITS %s %s'%('.'*20, ecmd('sc config BITS start= disabled')==0)
    print 'Renaming SoftwareDistribution %s %s'%('.'*20, ecmd(rn)==0)
    print 'Enabling Windows Update Service %s %s'%('.'*20, ecmd('sc config wuauserv start= auto')==0)
    print 'Starting Windows Update Service %s %s'%('.'*20, ecmd('net start wuauserv')==0)
    print 'Enabling BITS %s %s'%('.'*20, ecmd('sc config BITS start= auto')==0)
    print 'Starting BITS %s %s'%('.'*20, ecmd('net start BITS')==0)
    if os.path.isdir(p):
        print '%s %s is available again'%(p, '.'*20)
    else:
        print '%s %s is not available again!!'%(p, '.'*20)
    if os.path.isdir(pn):
        print 'Removing the renamed Folder %s %s True'%(pn, '.'*20)
        shutil.rmtree(pn)

def ecmd(CMD):
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
    ret=OBJ.returncode
    return ret
try:
    import _winreg
    key = getattr(_winreg,"HKEY_LOCAL_MACHINE")
    subkey = _winreg.OpenKey(key, "SYSTEM\CurrentControlSet\Control\Session Manager" )
    (value, type) = _winreg.QueryValueEx(subkey,"PendingFileRenameOperations")
    if value != "":
		print 'There is no pending updates in the system'
		print 'Deleting windows update files begins...'
		delete_update()        
    elif value == "":
		print 'Windows update process is in progress'
		print 'Please restart your machine to complete windows update process and then run this script to remove updates files'
		sys.exit()

except:
    delete_update()
        
       
