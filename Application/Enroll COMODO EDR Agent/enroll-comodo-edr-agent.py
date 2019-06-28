URL=itsm.getParameter('Enter_the_URL') # Enter the URL
FileName=itsm.getParameter('Enter_the_filename') # Give your FileName as it is in Drive and ensure downloaded filename and Uploaded filename has not changed.
Extension=itsm.getParameter('Enter_the_extension') # ENter the extension. For Eg: ".exe"
import urllib


fn = FileName+Extension

import os
import ctypes
import subprocess
import shutil,time
import ssl



class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


context = ssl._create_unverified_context()            

def Download(URL,fileName):
    import urllib2
    import os
    print "Download started"
    src_path=os.environ['ProgramData']
    fp = os.path.join(src_path, fileName)
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    if not os.path.exists(src_path):
        os.makedirs(src_path)
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    print "The file downloaded successfully in specified path"+fp
    try:
        print'Downloaded Application %s Installation Started'%fileName
        dr=os.popen(fp+' /quiet').read()
        print dr
        print '%s Application Successfully Installed'%fileName
    except:
        print 'No : '+fp+' is exist'


Download(URL,fn)
