destination_folder = r"C:\Users\comodo\Desktop" ##  Here mention the path where the application should be copied on endpoint
fromURL='http://download.piriform.com/ccsetup523.exe'## Here mention the download url

import os
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

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
Down_path=os.environ['PROGRAMDATA']
fileName = fromURL.split('/')[-1]
DownTo = os.path.join(Down_path, fileName)
def downloadFile(DownTo, fromURL):
    try:
        with open(DownTo, 'wb') as f:
            f.write(urllib.urlopen(fromURL).read())
        if os.path.isfile(DownTo):
            return '{} - {}KB'.format(DownTo, os.path.getsize(DownTo)/1000)
		
    except:
        return 'Please Check URL or Download Path!'

if __name__=='__main__':
    print downloadFile(DownTo, fromURL )
	

import shutil
try:
    shutil.copy2(DownTo, destination_folder)
    print("%s is copied to %s"%(DownTo, destination_folder))
    print "File copied successfully"
except Exception as err :
    print err
