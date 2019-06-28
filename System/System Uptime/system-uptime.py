import os
import time
import platform
import ssl
import subprocess
import shutil
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

Folder=os.environ['TEMP']+r"\Noproblem"
if not os.path.exists(Folder):
    os.mkdir(Folder)
fileName=r"uptime.exe"
src_path=Folder
fp = os.path.join(src_path, fileName)    
URL=r"https://drive.google.com/uc?export=download&id=1sp0wSczt8YGaGcoXjHtXBmKu90ITzbLM"
Excutable_path=Download(Folder, URL,fp)
time.sleep(20)
output=Folder+"\\"+fileName+" -h"
process=subprocess.Popen(output, shell=True, stdout=subprocess.PIPE)
result=process.communicate()[0]
print result
try:
    shutil.rmtree(Folder)
except:
    pass

