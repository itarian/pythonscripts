service="svchost" #please enter the active service or the process which needed to be monitored
x= 4 #please enter maximum memory space limit value in MegaBytes(MB)
y= 50 #please enter maximum cpu use percentage limit(range between [0-100])

import sys
def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg))

def convert2Bytes(s):
    data=s
    multi=1024
    return(data*multi*multi)
def convert2MBytes(s):
    data=s
    div=1024
    return(data/div/div)

import os   
lis=[]
lis1=[]
sum1=0
value=0
count=0
x=convert2Bytes(x)
if "Idle" in service:
    service="Idle"

cmd=os.popen("wmic path Win32_PerfFormattedData_PerfProc_Process get Name,PercentProcessorTime | findstr /i /c:%s"%(service)).read()
cper=len(cmd.splitlines())

if cper>1:
    lis=cmd.split()
    for i in xrange(1,len(lis),2):
        sum1=sum1+int(lis[i])
elif cper==1:
    lis=cmd.split()
    sum1=sum1+int(lis[1])
else:
    print"Please enter the valid service name"

cmd1=os.popen("wmic process get name,workingsetsize | findstr /i /c:%s"%(service)).read()
mem=len(cmd1.splitlines())

if mem>1:
    lis1=cmd1.split()
    for i in xrange(1,len(lis),2):
        value=int(lis1[i])
        if value>x:
            count=count+1
               
elif mem==1:
    lis1=cmd1.split()
    value=int(lis[1])
    if value>x:
        count=count+1

else:
    print"please enter the valid service name"

value=convert2MBytes(value)

if sum1>y or count>=1:
    print service+" Process exceeds the usage limit "
    alert(1)
else:
    print "The cpu percentage and memory used by process "+service+" is "+str(sum1)+" and "+str(value)+" MB"
    alert(0)
    
    
    





