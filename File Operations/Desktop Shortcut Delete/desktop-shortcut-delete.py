quick_icon_name=r'MuseScore 2.lnk' #provide the shortcut name with extention
import os
import getpass
path=r'C:\Users\Public\Desktop'
found=0
path1=getpass.getuser()
path1=os.path.join('C:\Users',path1,'Desktop')
def ecmd(command):
    import ctypes
    from subprocess import PIPE, Popen
    
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
        obj = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()
    ret=obj.returncode
    if ret==0:
        if out:
            return out.strip()
        else:
            return ret
    else:
        if err:
            return err.strip()
        else:
            return ret
for i in os.listdir(path):
    if quick_icon_name.lower() == i.lower():
        cmd1='del '+'"'+path+'\\'+quick_icon_name+'"'
        print ecmd(cmd1)
        if os.path.isfile(os.path.join(path, i)):
            print 'Removing the Quick Icon "%s" is Failed'%quick_icon_name
        else:
            found+=1
            print 'The Quick Icon "%s" is Removed'%quick_icon_name
    else:
        found+=0

for i in os.listdir(path1):
    if quick_icon_name.lower() == i.lower():
        cmd1='del '+'"'+path1+'\\'+quick_icon_name+'"'
        print ecmd(cmd1)
        if os.path.isfile(os.path.join(path1, i)):
            print 'Removing the Quick Icon "%s" is Failed'%quick_icon_name
        else:
            found+=1
            print 'The Quick Icon "%s" is Removed'%quick_icon_name
    else:
        found+=0


if not found:
    print 'The Quick Icon "%s" does not Exist\n'%quick_icon_name
print("--------------------------------------------------------")
print("The remaining  Quick Icons in Windows Desktop are")
applist=os.listdir(path)
for i in applist:
    if i.endswith('.lnk'):
        print i
