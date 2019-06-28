url="https://shield.dome.comodo.com/api/agent/download/S1TpT0Pqf" # Provided the URL to download the Dome shield agent
#Get the download link from Download agent > "ITSM Agent Download link"
a=url.split("/")[-1]
import os
import time
import ctypes

path=os.environ['TEMP']
filepath=path+r'\cShieldAgent_%s_installer.msi'%a
command= 'msiexec.exe /i cShieldAgent_%s_installer.msi /qn'%a


class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

def Download(filepath,url):
    import urllib2
    import os
    import ssl
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    try:
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        parsed = urllib2.urlopen(req,context=gcontext)
    except:
        parsed = urllib2.urlopen(req)
    
    with open(filepath, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    if os.path.exists(filepath):
        return filepath
    return False


Download(filepath,url)
print "Cdome shield Roaming agent has been downloaded from ",url


with disable_file_system_redirection():
        os.chdir(path)
        os.popen(command)
        time.sleep(5)      

print "Cdome shield Roaming agent has been installed"	

try:
    os.remove(filepath)	
except: 
    pass
def reboot():
    print "restarting .............."
    os.popen("shutdown -r -t 00").read()
reboot()
