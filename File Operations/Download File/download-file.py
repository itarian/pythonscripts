DownTo='C:\Users\Meteor\Desktop' ##  Here mention the path where the application to download
fromURL='http://download.piriform.com/ccsetup523.exe' ## Here mention the download Link
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

import subprocess        
with disable_file_system_redirection(): 
        import urllib
import os

def downloadFile(DownTo, fromURL):
    try:
        fileName = fromURL.split('/')[-1]
        DownTo = os.path.join(DownTo, fileName)
        with open(DownTo, 'wb') as f:
            f.write(urllib.urlopen(fromURL).read())
        if os.path.isfile(DownTo):
            return '{} - {}KB'.format(DownTo, os.path.getsize(DownTo)/1000)
    except:
        return 'Please Check URL or Download Path!'

if __name__=='__main__':
    print downloadFile(DownTo, fromURL )
