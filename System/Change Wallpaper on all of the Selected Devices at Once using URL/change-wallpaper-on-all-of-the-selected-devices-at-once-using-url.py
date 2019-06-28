URL=r'https://drive.google.com/uc?export=download&id=1itfPNf3G4DkcpWh6_V4E0MJHtE2BZ2WP' #Provide the url which you need to download
fileName = r'images.jpeg' #Provide the filename of the image along with extension.
import _winreg
import os
import ctypes
import shutil
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
workdir=os.environ['PROGRAMDATA']+r'\temp'
shutil.rmtree(workdir,ignore_errors=True)
fileName = r'images.jpeg'

if not os.path.exists(workdir):
     os.mkdir(workdir) 
def Download(workdir, URL):
    import urllib2
    import os
    fileName = r'images.jpeg'
    fp = os.path.join(workdir, fileName)
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    if os.path.exists(workdir):
        if not os.path.exists(workdir):
            os.makedirs(workdir)
        
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    
    
    return fp

Download(workdir, URL)
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

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


path=workdir+"\\"+fileName
print path
handle = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,"Control Panel\Desktop",0,_winreg.KEY_ALL_ACCESS)
_winreg.SetValueEx(handle, "Wallpaper", 0, _winreg.REG_SZ, path)
print "Updating the wallpaper images..."
print 'Restarting the endpoint to apply changes ....'
print ecmd('shutdown -r -t 00')
