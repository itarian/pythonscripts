IP_ADDRESS =r"CHANGE_ME"## Here mention the IP_ADDRESS for DLP installation
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

def os_platform():
    true_platform = os.environ['PROCESSOR_ARCHITECTURE']
    try:
            true_platform = os.environ["PROCESSOR_ARCHITEW6432"]
    except KeyError:
            pass
            #true_platform not assigned to if this does not exist
    return true_platform

Folder=os.environ['TEMP']+r"\Noproblem"
if not os.path.exists(Folder):
    os.mkdir(Folder)
fileName=r"endpoint-win-3.12.2.msi"
src_path=Folder
fp = os.path.join(src_path, fileName)    
URL=r"http://download.comodo.com/mydlp/ep/endpoint-win-3.13.2.msi"
Excutable_path=Download(Folder, URL,fp)
output="msiexec /i "+Excutable_path+" /quiet /qn /norestart management_server="+IP_ADDRESS
process=subprocess.Popen(output, shell=True, stdout=subprocess.PIPE)
result=process.communicate()
try:
    shutil.rmtree(Folder)
except:
    pass
print "Comodo DLP agent installed Successfully"
