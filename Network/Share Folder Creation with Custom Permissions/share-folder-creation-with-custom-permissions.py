a=1 #set a=1 to give full access
    #set a=2 to give only read access
    #set a=3 to give change access
path=r'C:\me'#provide the path to create share
sharename=r'Public3' #share name should be modified each time
username=r'Everyone'#default is everyone
import os

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
if not os.path.exists(path):
    os.mkdir(path,0777)
else:
    pass
if a==1 :
    print ecmd('net share '+sharename+'='+path+' /GRANT:'+username+',FULL')
if a==2 :
    print ecmd('net share '+sharename+'='+path+' /GRANT:'+username+',READ')
if a==3 :
    print ecmd('net share '+sharename+'='+path+' /GRANT:'+username+',CHANGE')
