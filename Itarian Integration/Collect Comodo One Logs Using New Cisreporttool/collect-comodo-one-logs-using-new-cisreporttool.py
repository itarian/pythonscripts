def Download():
    import urllib2
    import os
    import subprocess

    URL='http://download.comodo.com/cis/download/installs/cisreporttool/cisreporttool.exe'
    fileName =URL.split('/')[-1]
    src_path=os.environ['ProgramData']
    fp = os.path.join(src_path, fileName)
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    parsed = urllib2.urlopen(request)
    
    if os.path.exists(src_path):
        
        if not os.path.exists(src_path):
            os.makedirs(src_path)
        
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            
            if chunk:
                f.write(chunk)
            else:
                break
    
    print "Report collection has started..."
    process= subprocess.Popen(fp, shell=True, stdout=subprocess.PIPE)
    result=process.communicate()
    
    if "upload successed" in result[0]:
        print "Report collection is successfull"

        try:
         d1=os.listdir(src_path)
         os.remove(os.path.join(src_path,"cisreporttool.exe"))

        except:
            pass
         
        try:
            d=os.listdir(src_path)
            for i in d:
                if "CisReportData" in i:
                    os.remove(os.path.join(src_path,i))
        except:
            pass
            
    else:
        print "Failed to collect report"
        
        
Download()
