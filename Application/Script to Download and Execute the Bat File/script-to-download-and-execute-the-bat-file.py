Folder_name=r"Vicky"                               # Give the new folder name 
Folder_Path=r"C:\Users\rainbow\Desktop"            # Provide Path for the New folder 
URL=r'https://drive.google.com/uc?export=download&id=1o6EspNx2FiwfD2etKLgtd-p9GEXvp_9Q' # Provide the direct download link for the BAT file
File_name=r"multi.bat" #Provide the Bat file name with extension
directory=Folder_Path+"\\"+Folder_name

import os
import subprocess        
import urllib
import ctypes

if not os.path.exists(directory):
    os.makedirs(directory)

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

def Download(src_path, URL,fp):
    import urllib2
    
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    try:
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        parsed = urllib2.urlopen(request,context=gcontext)
    except:
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
    return fp

def bat(path):
    print path
    with disable_file_system_redirection():
        print "Excuting Bat File"
        process = subprocess.Popen([path],stdout=subprocess.PIPE)
        stdout = process.communicate()[0]
        print "---------------------------"
        print stdout
            
if __name__=='__main__':
    import time
    fp = os.path.join(directory, File_name)
    path=Download(directory, URL,fp)
    print path
    time.sleep(10)
    bat(path)
    
