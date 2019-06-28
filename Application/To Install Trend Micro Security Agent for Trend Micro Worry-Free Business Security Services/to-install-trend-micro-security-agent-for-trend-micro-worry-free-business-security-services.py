URL=r'https://onedrive.live.com/download?cid=A910C8EF113350FB&resid=A910C8EF113350FB%21114&authkey=AEDUDPZMBM6SlVI' #provide a direct URl to download the agent package
IDENTIFIER=r"X3a2kF4T3y6bPNBqTDKLw2aRbUH86ThMRKFU3O3BBFPx/KixMPIQtSc+oJPabFbU2fNuNA81KbhloYmrccLa1gW+7JNTgCuTAjJ66cNiO3r0SDnIOqyK7wWEFZ0CsRgv"#provide a identifier to enroll the device into a other group or accounts
import os
check=os.popen("wmic product get name").read()

if "Trend Micro Security Agent" in check:
    print "Trend Micro Security Agent already installed at the endpoint"
else:
    import urllib2
    import ssl
    fileName =r"WFBS-SVC_Agent_Installer.msi"
    src_path=os.environ['PROGRAMDATA']
    fp = os.path.join(src_path, fileName)
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
    if os.path.exists("C:\Program Files\Trend Micro"):
        import shutil
        shutil.rmtree("C:\Program Files\Trend Micro")
    else:
        pass

    cmd=fp+' /qn'+' IDENTIFIER="%s"'%(IDENTIFIER)
    install=os.popen(cmd).read()
    check1=os.popen("wmic product get name").read()
    if "Trend Micro Security Agent" in check1:
        print 'Trend Micro Security Agent Successfully Installed At The Endpoint'
    else:
        print "Installation failed,do restart the Endpoint and try again"


try:
    os.remove(fp)
except:
    pass


