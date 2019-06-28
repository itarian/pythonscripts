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
out=[]
out=os.popen('WMIC product get name,version').read()
out=out.replace("COMODO Client - Communication Updater",'')
out = out.split("\r\n")
for i in out:
    if 'COMODO Client - Communication'in i:
        fi = i
        k=fi.split()
        fi=k[4].replace('.','')
        fi.replace(' ','')
        try:
            fi=float(fi)
        except ValueError,e:
            print fi
        
        if fi >= 6.17:
            print ecmd('wmic product where name="COMODO Client - Communication Updater" call uninstall')
        else:
            print "COMODO Client - Communication  is  older version"


    
	
