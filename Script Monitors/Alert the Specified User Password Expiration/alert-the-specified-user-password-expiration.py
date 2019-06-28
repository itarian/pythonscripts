
import os,ctypes,re,sys
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

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg))

output_format = '%m/%d/%Y'
dt_time=get_date(output_format)
d=[]

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
    alert(1)
    print '\n'

else:
    print "User doesnt need to reset the password"
    alert(0)
    
    

    
