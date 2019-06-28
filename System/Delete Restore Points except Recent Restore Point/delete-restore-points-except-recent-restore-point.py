import os
import re
drive= os.environ['SYSTEMDRIVE']
import re
def ecmd(CMD, r=True):
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
    ret=OBJ.returncode
    
    if r:
        return ret
    else:            
        if ret==0:
            return out
        else:
            return ret

rp_count=ecmd('vssadmin List Shadows /for=%s'%drive,False)
A=ecmd('vssadmin List Shadows /for=%s'%drive,False)

if A == 1:
    print "There is no restore point created in this system"
else:
    b=re.findall('(Contents\sof\sshadow\scopy\sset\sID:\s.*)',A)
    if rp_count == 1:
        print 'No restore points are created in your system'
    elif len(b)==1:
        print 'ONLY ONE RESTORE POINT (and) NO OLD RESTORE POINTS PRESENT IN YOUR SYSTEM'
    else:
        print 'RESTORE POINTS PRESENT IN YOUR SYSTEM IS:'
        print rp_count
        print '\n'
        #deleteOLD_rp
        print 'DELETING OLDEST RESTORE POINTS IN YOUR SYSTEM..........'
        print '\n'
        print 'AFTER REMOVAL OF OLD RESTORE POINTS ..................................'
        def ecmd(CMD, r=True):
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
            ret=OBJ.returncode
            
            if r:
                return ret
            else:            
                if ret==0:
                    return out
                else:
                    return ret
        for i in range(1,(len(b))):    
            ecmd('vssadmin delete shadows /for=%s /oldest /quiet'%drive,False)
        
        fin=ecmd('vssadmin List Shadows /for=%s'%drive,False)
        print fin
