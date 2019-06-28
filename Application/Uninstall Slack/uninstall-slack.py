import os
import ctypes
from subprocess import PIPE, Popen



URL=r'https://drive.google.com/uc?authuser=0&id=140mlfpTzJ2rT7XZuwCfwbrjgzmbxv3an&export=download'
DownloadPath=os.environ['TEMP']
FileName=r'UninstallView'
Extension=r".exe"




## If pattern is given, converts to real path
def PaternPath(DownloadPath):
    import os
    if not os.path.isdir(DownloadPath):
        return ExecuteCMD('echo '+DownloadPath, True)
    return DownloadPath

## Downloads application
def Download(Path, URL, FileName,Extension):
    import urllib2
    import os
    fn = FileName + Extension
    fp = os.path.join(Path, fn)
    req = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    con = urllib2.urlopen(req)
    with open(fp, 'wb') as f:
        while True:
            chunk=con.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    if os.path.exists(fp):
        return fp
    return False


import os
##    print Path
Path=PaternPath(DownloadPath)
##    print FilePath
FilePath=Download(Path, URL, FileName,Extension)


if os.path.exists(Path):
    pf=FilePath 
    if os.path.isfile(pf):
        ec='"%s" /quninstall "Slack"'%pf

        OBJ = Popen(ec, shell = True, stdout = PIPE, stderr = PIPE)
        out, err = OBJ.communicate()
        RET = OBJ.returncode

        if RET == 0:
            print "Slack is uninstalled from endpoint"

        else:
            print "Slack is not uninstalled"
     
