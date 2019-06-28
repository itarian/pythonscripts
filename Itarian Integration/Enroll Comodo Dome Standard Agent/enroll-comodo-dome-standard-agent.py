filename=r'DomeSWGAgent_ad0da3f73a_Installer'# The file name you mentioned here should match with the file name in drive where you saved the file. 
cdome_url=r'https://drive.google.com/uc?id=1DPK1EA8DsFVPPlJUCePV1nfQYYp9sw_O&export=download'    # Dome standard agent requires authentication to download the package.
# For convenience we have provided the package in a safe google drive and the URL for the google drive is attached here.
# You can place the package whereever you want and you can download from that path.

import os

def Download(Path, URL, FileName, Extension):
    import urllib2
    import os
    import ssl
    fn = FileName+Extension
    fp = os.path.join(Path, fn)
    try:
        req = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
        parsed = urllib2.urlopen(request)
    except:
        req = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        parsed = urllib2.urlopen(req, context=gcontext)
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    if os.path.exists(fp):
        return fp
    return False

def wincmd(command):
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
        ret= obj.returncode
        if ret == 0:
            return(out)  
        return False   


def c1temp():
    temp=os.environ['PROGRAMDATA']+'\c1_temp'
    if os.path.exists(temp):
        pass
    else:
        os.mkdir(temp)
    return(temp)

temp=c1temp()

print 'Downloading Cdome agent..'
down_path=Download(temp,cdome_url,filename,r'.exe')		

if down_path:
    print 'Cdome agent installation begins...'
    wincmd(down_path+ ' /S')
    print 'Cdome agent installed at your endpoint'
else:
    print 'Cdome agent failed to dowload. Please check'
    sys.exit()

print ' Done ..'

def remove():
    try:
        os.remove(temp)
    except:
        pass
remove()
def reboot():
    print "restarting .............."
    os.popen("shutdown -r -t 00").read()
reboot()
