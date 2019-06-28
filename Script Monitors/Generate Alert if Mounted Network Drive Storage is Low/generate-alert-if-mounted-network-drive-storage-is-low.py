import sys
import os
import re
def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))

def humanbytes(B):
   'Return the given bytes as a human friendly KB, MB, GB, or TB string'
   B = float(B)
   KB = float(1024)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)

lis=[]
count=0
detected_drives=os.popen('wmic logicaldisk get description,name | findstr /i /c:Network ').read()
local_drive=re.findall('[A-Z]:',detected_drives)
for j in local_drive:
    cmd=os.popen('fsutil volume diskfree '+j).read()
    total_space=re.findall('Total\s\W\sof\sbytes(.*)',cmd)
    free_space=re.findall('Total\s\W\sof\sfree\sbytes(.*)',cmd)
    d=free_space[0].split()
    e=total_space[0].split()
    i=int(d[1])
    print i
    k=int(e[1])
    threshold=20*(k/100)
    print threshold
    print "\n Total size of the Network drive "+j+humanbytes(k)
    print "Free space in the Network drive "+j+humanbytes(i)
    if i<=threshold:
        lis.append(j)
        count=count+1

if count>=1:
    for i in lis:
        print "\n Low storage alert in Network Drive "+i
    alert(1)
elif local_drive==[]:
    print "No network drives detected in the system"
    
else:
    print "Network Drives storage is normal"
    alert(0)
