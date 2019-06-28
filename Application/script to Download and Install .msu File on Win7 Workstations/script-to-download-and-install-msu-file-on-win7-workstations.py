import os
import ctypes
import sys
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

src_path=os.environ['TEMP']

class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)

if 'PROGRAMW6432' in os.environ.keys():
        URL=r'http://download.windowsupdate.com/d/msdownload/update/software/secu/2018/01/windows6.1-kb4056897-x64_2af35062f69ce80c4cd6eef030eda31ca5c109ed.msu'   # 64 Bit Download url
else:
        URL=r'http://download.windowsupdate.com/d/msdownload/update/software/secu/2018/01/windows6.1-kb4056897-x86_bb612f57e082c407b8cdad3f4900275833449e71.msu'   # 32 Bit Download url

def Download(src_path,URL):
    import urllib2
    import os
    print "Download started"
    fileName = 'windows6.1-kb4056897.msu'  # File Name (Edit your preferred file name)
    fp = os.path.join(src_path, fileName)
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    if os.path.exists(src_path):
        print "Path already exists"
    if not os.path.exists(src_path):
        os.makedirs(src_path)
        print "Path created"
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    print "The file downloaded successfully in "+src_path
    return fp

def install(fp):
    print fp
    sCMD=fp+' '+r'/quiet /norestart'
    if os.path.exists(fp):
        try:
            cmd = os.popen(sCMD).read()
            print cmd
            print 'Successfully Installed'
        except Exception as e:
            return e       
    else:
        return 'No path: '+path+' is exist'

fp=Download(src_path,URL)
print fp
install(fp)
