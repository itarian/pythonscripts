password="********"  ## password setup is based on policy requirement. the complex policy does not accept the simple password!

import os
import subprocess
from subprocess import PIPE, Popen

gt=[]
gf=[]

try:
    wdir=os.environ['PROGRAMDATA']+'\temp'
    if not os.path.exists(workdir):
            os.mkdir(workdir)
except:
    wdir=os.environ['SYSTEMDRIVE']

fp=wdir+'\\users.txt'
cmd="wmic useraccount get name"
obj=subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
out, err = obj.communicate()

with open(fp, 'w+') as dr:
    dr.write(out)

with open(fp, 'r+') as dr:
    for i in dr: None if 'Name' in i or 'DefaultAccount' in i or 'Guest' in i or 'Administrator' in i else gt.append(i.strip())

for i in filter(None, gt):
    obj = subprocess.Popen('net user "%s" "%s"'%(i, password), shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, err = obj.communicate()
    print "Password changed successfully for the user : "+i if out else err

try:
    os.remove(fp)
except:
    pass

print "Restarting the Machine to apply changes"
os.popen("shutdown.exe -r")
