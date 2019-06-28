new="carat"   ## Provide the name you want to rename your computer

import os
import re
import sys
old=os.popen("hostname").read()
name=old.strip('\n')
cmd=('WMIC computersystem where caption="%s" rename '+new)%(name)
cmd1=os.popen(cmd).read()
print cmd1
if cmd1=='':
    print "you do not have permission to change computer name"
    sys.exit()
else:
    fin=re.findall("Executing",cmd1)
    f=''.join(fin)
def value():
    if (b==0):
        print('success...renamed computer name to '+ new)
        print('your system will restart now for updating the changes')
        res=os.popen('shutdown -r').read()

    elif(b==5):
        print('Returnvalue is 5')
        print('run the script as System user')

    elif(b==1355):
        print('Returnvalue is 1355')
        print('Switch on the domain connected to the computer ')

    else:
        print('Failed to rename computer name')
    
try:
    if "Executing"  in f:
        alter=re.findall("ReturnValue =(.*);",cmd1)
        a=''.join(alter)
        b=int(a)
        value()

except:
    if "Executing" not in f:
        print("you do not have permission to change computer name")




