import os
import re
import time
import sys
import ctypes
from datetime import datetime

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg))
   

def check():
    inst=os.popen("wmic product get name,identifyingnumber").read()
    return inst

check()
inst=check()
ale=0
find=re.findall('{.*}\s\sCOMODO\sClient\s-\sSecurity',inst)
if len(find)==0:
    print "\nComodo Client Security is not installed at End point\n"
else:
    print "\nComodo Client Security is installed at End point\n"

    ki=os.popen('wmic process').read()
    if "cis.exe" in ki:
        print "Comodo Client Security is in running state"
        ale=0
    else:
        print "Comodo Client Security is not in running state"
        ale=ale+1

if ale==0:
    alert(0)
else:
    alert(1)
