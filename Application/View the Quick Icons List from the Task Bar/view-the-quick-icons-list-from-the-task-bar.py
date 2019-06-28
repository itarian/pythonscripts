import os
user = os.environ["APPDATA"]
path= user +'\\Microsoft\\Internet Explorer\\Quick Launch\\User Pinned\\TaskBar\\'
f1=os.listdir(path)
applist=os.listdir(path)
print 'The Files in Quick Bar are: '
for i in range(len(applist)+1):
    print i+1,'.', applist[i].replace('.lnk','')
    if i+1 == len(applist):
        break
