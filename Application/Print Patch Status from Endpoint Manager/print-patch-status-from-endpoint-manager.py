import os
import re
import random
import socket

b=[]
e=[]
def getrmm(a):
    os.chdir(a)
    c=os.popen("dir").read()
    find=re.findall('SpmAgent.*',c)
    
    
    for i in find:
        b.append(a+'\\'+i)
        
    
       
    for i in b:
        with open (i, 'r+') as file:
            for line in file:
                string=''
                line=line.strip()
                if 'Error' in line or 'Operation' in line or 'exit code' in line:
                   line=line+'\n'
                   if line=='':
                       continue
                   else:
                       line=line.strip()
                       string+=''.join(line)
                   print string
    cat=os.stat(i).st_size
    if cat==0:
        print 'File has empty Logs'
                   


if 'PROGRAMFILES(X86)' in os.environ.keys():
    pmlpath=os.path.join(os.environ['PROGRAMFILES(X86)'], 'COMODO\\Comodo ITSM\\cpmlogs')
else:
    pmlpath=os.path.join(os.environ['PROGRAMFILES'], 'COMODO\\Comodo ITSM\\cpmlogs')
    

getrmm(pmlpath)
