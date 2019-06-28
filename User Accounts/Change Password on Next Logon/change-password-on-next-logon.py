#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('parameterName') with that parameter's 
thresold="2019/9/1" #"%yyyy/%mm/%dd"
s=[]
val=[]
value1=[]
fnl=[]
fl=0
ps_command=r'get-aduser -filter * -properties passwordlastset | sort name | ft Name, passwordlastset'
def alert(arg): 
	sys.stderr.write("%d%d%d" % (arg, arg, arg))
import os,sys
k=os.popen('powershell "%s"'%ps_command).read()
import datetime
for i in k.split('\n'):
    s.append(i)
s=filter(None,s)    
for i in s[2:]:
    if not 'DefaultAccount' in i :
        if not 'Guest' in i:
            val.append(i)
val_thres=thresold.split('/')
d1 = datetime.datetime(int(val_thres[0]), int(val_thres[1]),int(val_thres[2]))            
val=filter(None,val)
for i in range(0,len(val)):
        k1=val[i].split()
        if len(k1) > 1 :         
         value1.append(k1[0])
         value1.append(k1[1])
        
print "LIST OF USERS PASSWORD LAST SET EXCEEDS AND THE FOLLOWING USER MUST CHANGE PASSWORD ON NEXT LOGON:...."
if value1:
    for i in range(0,len(value1)):
        if i%2!=0:
            if not value1[i]=='':
                val_user=value1[i].split('/')
                d2 = datetime.datetime(int(val_user[2]), int(val_user[0]),int(val_user[1]))
                if d2 <= d1:
                    print "\t*)",value1[i-1]
                    fnl.append(value1[i-1])
                    cmd='powershell "Get-ADUser -Identity %s | Set-ADUser -ChangePasswordAtLogon:$True"'%value1[i-1]
                    os.popen(cmd).read()
                else:
                    fl=1

            
else:
    print "\t*)","THERE IS NO USERS EXCEEDS PASSWORD LAST SET THRESHOLD...."

if fl==1:
    print "\t*)","THERE IS NO USERS EXCEEDS PASSWORD LAST SET THRESHOLD...."
if len(fnl)!=0:
    alert(1)
else:
    alert(0)
