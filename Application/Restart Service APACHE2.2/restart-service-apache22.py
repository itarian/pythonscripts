import subprocess
import os
import platform

drive=os.environ['SYSTEMDRIVE']
path=drive+r'\Program Files\Apache Software Foundation\Apache2.2\bin'
def getTasks(name):
    r = os.popen('tasklist /v').read().strip().split('\n')
    for i in range(len(r)):
        s = r[i]
        if name in r[i]:
            return r[i]
    return []

imgName = 'httpd.exe'

notResponding = 'Not Responding'

r = getTasks(imgName)

if r:
    print('%s is Running or Unknown' % (imgName))
    print path
    os.chdir(path)
    print os.popen('httpd.exe -k stop').read()
    print "Apache service Restarted successfully"


else:
   print('%s - No such process' % (imgName)) 




if os.path.exists(path):
    print path
    os.chdir(path)
    print os.popen('httpd.exe -k restart').read()
    print "Apache service Restarted successfully"
