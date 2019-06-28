#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('variableName') with that parameter's name
User_Name=itsm.getParameter('Username') ## Provide the User name
Domain=itsm.getParameter('Domain') ## Provide the Domain
First_Name=itsm.getParameter('First_Name') ## Provide the First name of the user
Last_Name=itsm.getParameter('Last_Name') ## Provide the Last name of the user
import os
import ctypes
import string
import random
import subprocess
from subprocess import PIPE, Popen
import re
import shutil

try:
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.exists(workdir):
        os.mkdir(workdir)      
except:
    workdir=os.environ['SYTEMDRIVE']


    
bat_file=workdir+r'Bat_file.bat'

content='''start cmd.exe /c "secedit /export /cfg C:\\ProgramData\\temp\\group-policy.inf /log export.log"
'''
y=Domain.split(".")
s=[]
for i in range(len(y)):
    s.append(" DC="+y[i])
ii=','.join(s)
with open(bat_file, 'w+') as fr:
    fr.write(content)

def remove():
    try:
        os.remove(workdir+"\\group-policy.inf")
        os.remove(workdir+"\\test.txt")
        
    except:
        pass   

def pw_gen_spl(size, chars=string.ascii_uppercase + string.digits + string.punctuation + string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))

def create():
    xx='dsadd user "CN=%s, CN=Users,%s" -fn %s -ln %s -disabled no -pwd %s -mustchpwd yes' %(User_Name, ii, First_Name, Last_Name, Password)
    print xx
    print "Temporary password :"+Password
    yy=os.popen(xx).read()
    print yy
    remove()

obj = subprocess.Popen(bat_file, shell = True, stdout = PIPE, stderr = PIPE)
out, err = obj.communicate()
print err
path="C:\\ProgramData\\temp\\group-policy.csv"
if os.path.isfile("C:\\ProgramData\\temp\\group-policy.inf"):
    with open("C:\\ProgramData\\temp\\group-policy.inf",'r') as f:
        with open('C:\\ProgramData\\temp\\test.txt','w+') as wr:
            k= f.read().decode('utf-16')
            k1=wr.write(k)
            
    with open("C:\\ProgramData\\temp\\test.txt",'r') as f:
        k=f.readlines()[5:8]
    header=[]
    value=[]
    for i in k:
        header.append(i.split('=')[0].strip())
        value.append(i.split('=')[1].replace('\n','').strip())
    if int(value[1])==1:
        val=int(value[0])+1
        Password=(pw_gen_spl(val, chars=string.ascii_uppercase + string.digits + string.punctuation + string.ascii_letters))
        create()
    else:
        val=int(value[0])+1
        Password=(pw_gen_spl(val, chars=string.ascii_uppercase + string.digits + string.punctuation + string.ascii_letters))
        create()      
            
else:
    
    Password=(pw_gen_spl(8, chars=string.ascii_uppercase + string.digits + string.punctuation + string.ascii_letters))
    xx='dsadd user "CN=%s, CN=Users,%s" -fn %s -ln %s -disabled no -pwd %s -mustchpwd yes' %(User_Name, ii, First_Name, Last_Name, Password)
    print "Temporary password :"+Password
    yy=os.popen(xx).read()
    print yy
    remove()

