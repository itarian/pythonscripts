URL=itsm.getParameter('Enter_the_URL')# Enter the URL
silent=itsm.getParameter('Enter_the_silent_command')#Enter the silent command for this application
def Download(URL,silent,):
    import urllib2
    import os
    print "Download started"
    fileName =URL.split('/')[-1]
    src_path=os.environ['ProgramData']
    fp = os.path.join(src_path, fileName)
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    if os.path.exists(src_path):
        print "Path already exists"
    if not os.path.exists(src_path):
        os.makedirs(src_path)
        print "Path created"
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
        os.popen(fp+' '+silent).read()
        print '%s Application Successfully Installed'%fileName
    except:
        return 'No : '+fp+' is exist'


Download(URL,silent)
