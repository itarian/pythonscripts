import os
import sys
ad=os.popen('net user').read()
import re
reg=re.findall('-\n(.*\n(.*))\n(.+)',ad)
st1=str(reg)
li=[]
for i in range(0,len(st1)-1):
    if st1[i]!=' ':
        li.append(st1[i])
        i=i+1
    else:
        if st1[i]==' ':
            i=i+1
            if st1[i]!=' ':
                li.append(' ')

x=''.join(li)
c=x.split(',')
c[0]
li=[]
fin_user=[]
st2=str(c[0])
fin=st2.split(' ')
for x in range(0,len(fin)-1):
    li.append(fin[x].strip('[(').strip("'").strip('\\n').strip('""'))

fin_user=[i for i in li if not i in ['DefaultAccount', 'Guest']]
def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))
def all_users(wrd):
    global ale
    ale=0
    
    wrd=str(wrd)+'\\'
    import sys
    import getpass
    import socket
    import _winreg
    fin=r'C:\Users\%sDocuments\Outlook Files'%wrd
    print "USER NAME: "+getpass.getuser()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print "IP-ADDRESS : "+(s.getsockname()[0])
    from time import gmtime, strftime
    time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print '\n'

    import os
    print fin
    if os.path.exists(fin):
        print('path is valid')
        try:
            os.chdir(fin)
            result=os.listdir(fin)
            print'Files are available'
            for i in result:
                b=os.path.getsize(i)
                print i +'\t'+ str(b)
            ale=ale+1
              
        except Exception as err:
            print err
            print'Please provide valid path'
            
            
    else:    
        print('Please provide right path')
for wrd in fin_user:
    all_users(wrd)

if ale>0:
    alert(1)
else:
    alert(0)
