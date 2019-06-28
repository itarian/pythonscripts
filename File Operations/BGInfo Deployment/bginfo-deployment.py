import os
path=r'C:\BGInfo'
URL=r'https://patchportal.one.comodo.com/portal/packages/spm/CCleanerPro/x86/ccsetup533pro.exe'
FileName=r'ccleanerpro'
Extension=r'.exe'
SilentCommand='/S'
print " Deploying "  +FileName+  "begins"
def Download(path, URL, FileName, Extension):
    import urllib2
    import os
    print "Download started"
    fn = FileName+Extension
    fp = os.path.join(path, fn)
    req = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    con = urllib2.urlopen(req)
    if os.path.exists(path):
        print "Path already exists"
    if not os.path.exists(path):
        os.makedirs(path)
        print "Path created"
    with open(fp, 'wb') as f:
        while True:
            chunk=con.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
Download(path, URL, FileName, Extension)
print "Download Completed"
def ExecuteCMD(CMD, OUT = False):
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
        RET = OBJ.returncode
        if RET == 0:
            if OUT == True:
                if out != '':
                    return out.strip()
                else:
                    return True
            else:
                return True
        return False

def Install(path, SilentCommand):
     fn = FileName+Extension
     fp = os.path.join(path, fn)
     if (fp[-4:-1]+fp[-1]).lower()=='.exe':
        return ExecuteCMD('"'+fp+'" '+SilentCommand)
     else:
        return ExecuteCMD('msiexec /i "'+fp+'" '+SilentCommand)

if Install(path, SilentCommand):
    print FileName+ "Installed sucessfully in" +path
else:
    print "Installation failed"

