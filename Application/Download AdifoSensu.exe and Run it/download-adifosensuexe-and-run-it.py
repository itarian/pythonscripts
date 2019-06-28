import os
import subprocess
import urllib2
import shutil
import ssl
SASToken = "?sv=2017-07-29&ss=f&srt=sco&sp=rl&se=2038-02-26T18:32:45Z&st=2018-02-25T10:32:45Z&spr=https&sig=3TLyzghRI5JFAhMJVi892pKA2rdMZYsKKX9nY31u6AE%3D"
CloudLocation = "https://adifosoftware.file.core.windows.net/software/Sensu/"
application = "AdifoSensu.exe"

url = CloudLocation + application + SASToken
print("Download url: " +url)
file_Path=os.path.join(os.environ['USERPROFILE'])
file_name=os.path.join(file_Path, application)
def Download(Path, URL, FileName):
    import urllib2
    import os
    print("Downloading " + application + " to " + file_name)
    fn = FileName
    fp = os.path.join(Path, fn)
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    try:
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        parsed = urllib2.urlopen(request,context=gcontext)
    except:
        parsed = urllib2.urlopen(request)
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
        return fp
    return False
Download(file_Path, url, file_name)
print "Download completed....."
if os.path.exists("c:\\opt"):
    try:
        os.chmod("c:\\opt",0777)
        shutil.rmtree("c:\\opt")
    except:
        pass
a= os.popen(file_name).read()
print a
if not "Error" in a:
    print "Sensu Client succesfully installed"
else:
    print 'Sensu Client installation failed'
