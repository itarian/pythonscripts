import os
import sys
def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg)) 

fp=[]
mm=[]
rtDir=os.environ['SYSTEMDRIVE']+'\\'
for root, dirs, files in os.walk(rtDir):
    for i in files:
        if i.endswith('.DMP'):
            fp.append(os.path.join(root,i))

            
ale=0
if fp:
    for i in fp:
        if 'MEMORY.DMP' in i or 'Memory.DMP' in i :
            k=i.split('\\')[-1]
            mm.append(i)
       

if mm:
    ale=ale+1
    print "MEMORY.DMP FILE FOUND IN THE SYSTEM...\n"
    for j,i in enumerate(mm,1):
        k=i.split('\\')[-1]
        print str(j)+'.'+k+' and is located at '+i+'\n'
                  
   
else:
    print "THERE IS NO MEMORY.DMP FILES FOUND IN THE SYSTEM...\n"



if ale>0:
    alert(1)

else:
    alert(0)
