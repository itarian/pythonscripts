import os
CMD=r"wmic useraccount get name"
out=os.popen(CMD).read()
try:
    for i in range(1,len(out.split())):
        try:
            CMD1=r"net user"+" "+out.split()[i]
            out1=os.popen(CMD1).read()
            print out1
        except:
            pass
except:
    pass
