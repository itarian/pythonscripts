import os
ApplicationName=r'Sophos Central (Cloud) Endpoint'
URL=r'https://drive.google.com/uc?authuser=0&id=1hSWicrFQ-Al0NfYjB8ETz9ryjtdtMK-_&export=download'
SilentCommand='-q'
DownloadPath=os.environ['TMP']
FileName=r'Sophos'
Extension=r".exe"


## Execute CMD
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
    if RET >= 0:
        if OUT == True:
            if out != '':
                return out.strip()
            else:
                return True
        else:
            return True
    return False

## If pattern is given, converts to real path
def PaternPath(DownloadPath):
    import os
    if not os.path.isdir(DownloadPath):
        return ExecuteCMD('echo '+DownloadPath, True)
    return DownloadPath

## Downloads application
def Download(Path, URL, FileName,Extension):
    import urllib2
    import os
    fn = FileName + Extension
    fp = os.path.join(Path, fn)
    req = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    con = urllib2.urlopen(req)
    with open(fp, 'wb') as f:
        while True:
            chunk=con.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    if os.path.exists(fp):
        return fp
    return False

## Install Application with Silent Command
def Install(FilePath, SilentCommand):
    return ExecuteCMD(FilePath+" "+SilentCommand,True)
    
import os
##    print Path
Path=PaternPath(DownloadPath)
##    print FilePath
FilePath=Download(Path, URL, FileName,Extension)


if Install(FilePath, SilentCommand):
    print ApplicationName+' .... installed successfully :)'
    os.remove(FilePath)
else:
    print ApplicationName+'.... not installed '


