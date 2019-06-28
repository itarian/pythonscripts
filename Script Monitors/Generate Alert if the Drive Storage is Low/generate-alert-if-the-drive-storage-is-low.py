import sys
import os
import re


def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))


def humanbytes(B):
    'Return the given bytes as a human friendly KB, MB, GB, or TB string'
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776

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


p = 0  # This constant contains result which will be transferred into the alert return value 

detected_drives = os.popen('wmic logicaldisk get description,name | findstr "Local" ').read()
local_drive = re.findall('[A-Z]:',detected_drives)
for j in local_drive:
    cmd = os.popen('fsutil volume diskfree '+j).read()
    total_space = re.findall('Total\s\W\sof\sbytes(.*)',cmd)
    free_space = re.findall('Total\s\W\sof\sfree\sbytes(.*)',cmd)
    d = free_space[0].split()
    e = total_space[0].split()
    i = int(d[1])
    k = int(e[1])
    threshold = 5*(k/100)
    print("Total size of the local disk " + j + humanbytes(k))
    print("Free space in the local disk " + j + humanbytes(i))
    if i <= threshold:
        print("Low storage alert in local disk "+j)
        p = 1
    else:
        pass

if p:
    alert(1)

else:
    alert(0)
