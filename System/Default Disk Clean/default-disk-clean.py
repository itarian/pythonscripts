import os
import subprocess
import sys
import shutil
import getpass
temp=os.environ['PROGRAMDATA']+r'\c1_temp'

if not os.path.exists(temp):
    os.makedirs(temp)

if 'PROGRAMW6432' in os.environ.keys():
    path=r'C:\Program Files (x86)\Wise\Wise Disk Cleaner'
    URL=r'http://downloads.wisecleaner.com/soft/WDCFree.exe'
else:
    path=r'C:\Program Files\Wise\Wise Disk Cleaner'
    URL=r'http://downloads.wisecleaner.com/soft/WDCFree.exe'

FileName=r'WiseDiskCleaner'
Extension=r'.exe'
SilentCommand='/VERYSILENT'
arch=os.environ['PROCESSOR_ARCHITECTURE']
print "Deploying "  +FileName+  " begins"


def Download(path, URL, FileName, Extension):
    import urllib2
    import os
    print "Download started"
    fn = FileName+Extension
    fp = os.path.join(path, fn)
    req = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    con = urllib2.urlopen(req)
    with open(fp, 'wb') as f:
        while True:
            chunk=con.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    return fp

print "Download Completed"

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
        if RET == 0:
            if OUT == True:
                if out != '':
                    return True
                else:
                    return True
            else:
                return True
            return False
        
def Install(fb, SilentCommand):
    if (ExecuteCMD('"'+fb+'" '+SilentCommand,True)):
        print FileName+ " Installed sucessfully in the system "      
        if os.path.exists(r'C:\Program Files\Wise\Wise Disk Cleaner\WiseDiskCleaner.exe'):
            return r'C:\Program Files\Wise\Wise Disk Cleaner\WiseDiskCleaner.exe'
        else: 
            return r'C:\Program Files\Wise\Wise Disk Cleaner\WiseDiskCleaner.exe'
    else:
        print FileName+' not installed properly. Please try again' 
        sys.exit()

def get_path():
    if 'PROGRAMW6432' in os.environ.keys():
        return r'C:\Program Files (x86)\Wise\Wise Disk Cleaner'
    else:
        return r'C:\Program Files\Wise\Wise Disk Cleaner'

def un_path():
    if 'PROGRAMW6432' in os.environ.keys():
        return r'C:\Program Files (x86)'
    else:
        return r'C:\Program Files'

def Clean(path):
    s=get_path()
    os.chdir(s)
    a=os.popen('WiseDiskCleaner.exe -a -adv').read()


def uninstall(path):
    if arch == 'AMD64':
        rem_reg_1=os.popen('reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Wise Disk Cleaner_is1" /f').read()
        print rem_reg_1
    else:
        rem_reg=os.popen('reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Wise Disk Cleaner_is1" /f').read()
        print rem_reg
    rem=os.popen(r"C:\Program Files\Wise\Wise Disk Cleaner\unins000.exe /SILENT").read()
    print rem
    print 'wise disk cleaner uninstalled'
    fn = FileName+Extension
    fp = os.path.join(path, fn)
    a=un_path()
    os.chdir(a)
    if a == r'C:\Program Files' :
        os.chdir(r'C:\Program Files')
        shutil.rmtree(r'C:\Program Files\Wise')
        shutil.rmtree(temp)
        print 'File removed from your system'
    elif a == (r'C:\Program Files (x86)'):
        os.chdir(r'C:\Program Files (x86)')
        shutil.rmtree(r'C:\Program Files (x86)\Wise')
        shutil.rmtree(temp)
        print 'File removed from your system'
    else:
        print 'file not removed from your system'
            
wise_status=Install(Download(temp, URL, FileName, Extension),SilentCommand)


if wise_status:
    Clean(wise_status)
    uninstall(path)
