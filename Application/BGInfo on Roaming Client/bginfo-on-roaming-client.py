S=r'/NoLicPrompt'
fn=r'BGInfo.zip'
fz=r'Bginfo.exe'
fromURL=r'https://download.sysinternals.com/files/BGInfo.zip' 
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import subprocess        
import ctypes
import zipfile
import ctypes
import urllib
import urllib2
import os
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
DownTo=os.environ['TEMP']
def Download(DownTo,fromURL, fn):
    fp = os.path.join(DownTo, fn)
    req = urllib2.Request(fromURL, headers={'User-Agent' : "Magic Browser"})
    con = urllib2.urlopen(req)
    with open(fp, 'wb') as f:
        while True:
            chunk=con.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    return fp
Download(DownTo,fromURL, fn)
print "Download Completed"
src_path=os.path.join(DownTo,fn)
dest_path=DownTo
path=os.path.join(DownTo,fz)
def filezip(src_path,dest_path):
    with disable_file_system_redirection():
        with zipfile.ZipFile(src_path,"r") as zip_ref:
            zip_ref.extractall(dest_path)
            print 'file unzipped to ' +dest_path 

filezip(src_path,dest_path)

with disable_file_system_redirection():      
    process=subprocess.Popen([path, S],stdout=subprocess.PIPE);
    result=process.communicate()[1]
    print "BGinfo succeessfully Displayed in endpoint"

