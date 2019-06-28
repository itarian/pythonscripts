import os
import urllib2
import math
import re
url='http://download.ccleaner.com/dfsetup221.exe'
silent='/S'

def Download(URL):
    import urllib2
    import os
    print "Download started"
    fileName =URL.split('/')[-1]
    src_path=os.environ['ProgramData']
    silent='/S'
    fp = os.path.join(src_path, fileName)
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    if os.path.exists(src_path):
        print "Path already exists"
    if not os.path.exists(src_path):
        os.makedirs(src_path)
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    print "The file downloaded successfully in specified path",fp
    try:
        print'Downloaded Application %s Installation Started'%fileName
        os.popen(fp+' '+silent).read()
        print '%s Application Successfully Installed'%fileName
        os.popen("del /Q 'C:\users\public\desktop\Defraggler.lnk'").read()
    
    except:
        return 'No : '+fp+' is exist'


def run(a):
    print 'Defragment tool started:'
    cmd=os.popen('wmic logicaldisk where drivetype=3 get name').read()
    ld=[i.strip() for i in cmd.split('\n') if i.strip()][1:]
    os.chdir(a)
    if ld:
        for i in ld:
            print os.popen('df.exe %s'%i).read()


a=os.path.join(r'C:\Program Files',r'Defraggler')
Download(url)   
run(a)
os.chdir(a)
print os.popen('uninst.exe'+' '+"/S").read()
