import getpass
import sys
from os import listdir
from os.path import isfile, join

username=getpass.getuser()
file_name=[]
email_address=[]
path="C:\Users\%s\AppData\Local\Microsoft\Outlook"%(username)
try:
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
except:
    print "Microsoft outlook is not installed in your device"
    sys.exit()


for i in onlyfiles:
    if ".tmp" in i or ".pst" in i or ".pab" in i or ".oab" in i or ".xml" in i or ".dat" in i or ".rwz" in i:
        continue
    else:
        file_name.append(i)

for i in file_name:
    if ".ost" in i:
        i=i.strip('ost')
        j=i.strip('.')
        email_address.append(j)
 
if len(email_address) >1:
    print "More than one email-ID is configured in '%s' user account"%(username)
    for i in email_address:
        print 'The outlook email address configured for user "%s" is "%s"'%(username,j)

else:
    print 'The outlook email address configured for user "%s" is "%s"'%(username,email_address[0])


    
