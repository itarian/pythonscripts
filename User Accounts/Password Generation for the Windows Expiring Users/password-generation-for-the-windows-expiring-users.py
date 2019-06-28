import os,ctypes,re,sys,string,subprocess
from subprocess import PIPE, Popen
import random
from datetime import datetime, date, time
user=os.popen("wmic useraccount get name").read()
l=[user]
m=l[0].split()
username=[]

def get_date(dateFormat="%m/%d/%Y"):
    import datetime
    timeNow = datetime.datetime.now()
    anotherTime1 = timeNow + datetime.timedelta(days=int(1))
    return anotherTime1.strftime(dateFormat)

output_format = '%m/%d/%Y'
dt_time=get_date(output_format)
d=[]
e=[]
f=[]
g=[]
count=0
newstring=""

for z in m:
    if 'Name' in z or 'Administrator' in z or 'DefaultAccount' in z or 'Guest' in z:
        pass
    else:
        username.append(z)

for i in username:
    a='net user ' +i+ ' /domain | find "Password expires"'
    b=os.popen(a).read()
    c=re.findall('Password expires             (.*)',b)[0]
    xyz=[x.strip() for x in c.split(',')][0]
    if (xyz.isalpha()) == True:
        count+=1
        
    elif (xyz.isalpha()) == False:
        count+=1
        
    v=count
    if v == 1:
        pass
    
    elif v!=1:
        if dt_time in xyz:
            d.append(i)
            a=1

        else:
            pass


if a==1:
    for k in d:
        xyz1=[x.strip() for x in k.split(',')][0]
        print "The specified User "+xyz1+" needs to reset the password"
        print '\n'
        print "Resetting the password for "+xyz1
        print '\n'


DomainName_1=os.popen('systeminfo | findstr /B /C:"Domain"').read()
DomainName2=re.findall('Domain:                    (.*)', DomainName_1)[0]
DomainName=DomainName2.strip('\n')

try:
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.exists(workdir):
        os.mkdir(workdir)      
except:
    workdir=os.environ['SYTEMDRIVE']
    
bat_file=workdir+r'Bat_file.bat'

content='''start cmd.exe /c "secedit /export /cfg C:\\ProgramData\\temp\\group-policy.inf /log export.log"
'''

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

def reset():
    y=DomainName.split(".")
    s=[]
    for i in range(len(y)):
        s.append(" DC="+y[i])
    ii=','.join(s)
    for i in d:
        xy1=[x.strip() for x in i.split(',')][0]
        xx='dsmod user "CN=%s, CN=Users,%s" -pwd %s -mustchpwd yes' %(xy1, ii, Password)
        obj = subprocess.Popen(xx, shell = True, stdout = PIPE, stderr = PIPE)
        out, err = obj.communicate()
        if out:
            print "Current Password is : "+Password
        if err:
            print err
    remove()

obj = subprocess.Popen(bat_file, shell = True, stdout = PIPE, stderr = PIPE)
out, err = obj.communicate()
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
        reset()
    else:
        val=int(value[0])+1
        Password=(pw_gen_spl(val, chars=string.ascii_uppercase + string.digits + string.punctuation + string.ascii_letters))
        reset()

else:
    print "Could not create Group policy file in specified directory"  
