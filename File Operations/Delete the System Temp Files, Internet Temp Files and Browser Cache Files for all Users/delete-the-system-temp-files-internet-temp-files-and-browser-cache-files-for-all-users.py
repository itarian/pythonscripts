#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('parameterName') with that parameter's name
import os
import subprocess        
import shutil
import ctypes

osdrive=os.environ['SystemDrive']
os_temp=osdrive+'\Windows\Temp'
x=[]
y=[]
def delete(src):
    try:
        if os.path.exists(src):
            if os.path.isdir(src):
                shutil.rmtree(src)
            elif os.path.isfile(src):
                os.remove(src)
        else:
            print '\t*)',"Error in the Source path"
    except:
        pass


print 'clearing files on the "%s" folder started:\n'%os_temp
f1=os.listdir(os_temp)
if f1:
    for i in f1:
        delete(os.path.join(os_temp,i))
    print '\t',"%s Cleared successfully"%os_temp
else:
    print '\t','No files found in the "%s"'%os_temp

print '\n'
rootpath=os.path.join(osdrive,'\Users')
a=os.listdir(rootpath)
for i in a:
        rootpath=osdrive+'\\Users'+'\\'+i
        if os.path.isdir(rootpath):
            x.append(rootpath)

for j in x:
    if os.path.exists(j):
        tmp=j+"\\"+'AppData\Local\Temp'
        y.append(tmp)
for i in y:
    if os.path.exists(i): 
        print 'clearing files on the "%s" folder started:\n'%i
        src=os.path.abspath(i)
        f2=os.listdir(i)
        if f2:
            for i in f2:
                delete(os.path.join(src,i))
            print '\t',"%s Cleared successfully"%i
        else:
            print '\t','No files found in the "%s"'%i

print '\n'
for i in x:
    chrome_path=i+"\AppData\Local\Google\Chrome\User Data\Default\Cache"
    if os.path.exists(chrome_path):
        print 'clearing files on the "%s" folder started:\n'%chrome_path
        f3=os.listdir(chrome_path)
        if f3:
            for i1 in f3:
                delete(os.path.join(chrome_path,i1))
            print '\t',"%s Cleared successfully"%chrome_path
        else:
            print '\t','No files found in the "%s"'%chrome_path
print '\n'
for i in x:
    fox_path=i+"\AppData\Local\Mozilla\Firefox\Profiles"
    if os.path.exists(fox_path):
        print 'clearing files on the "%s" folder started:'%fox_path
        f4=os.listdir(fox_path)
        if f4:
            for i2 in f4:
                delete(os.path.join(fox_path,i2))
            print '\t',"%s Cleared successfully"%fox_path
        else:
            print '\t','No files found in the "%s" \n'%fox_path

print '\n'    
for i in x:
    ie_path=i+"\AppData\Local\Microsoft\Windows\Temporary Internet Files\Low"
    if os.path.exists(ie_path):
        print 'clearing files on the "%s" folder started:\n'%ie_path
        f5=os.listdir(ie_path)
        if f5:
            for i3 in f5:
                delete(os.path.join(ie_path,i3))
            print '\t',"%s Cleared successfully"%ie_path
        else:
            print '\t','No files found in the "%s"'%ie_path

print '\n'
for i in x:
    ie_path=i+"\AppData\Local\Packages\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\AC\MicrosoftEdge\Cache"
    if os.path.exists(ie_path):
        print 'clearing files on the "%s" folder started:\n'%ie_path
        f5=os.listdir(ie_path)
        if f5:
            for i3 in f5:
                delete(os.path.join(ie_path,i3))
            print '\t',"%s Cleared successfully"%ie_path
        else:
            print '\t','No files found in the "%s"'%ie_path

print '\n'
ie_cache="RunDll32.exe InetCpl.cpl,ClearMyTracksByProcess 8 "

try:
    out=os.popen(ie_cache).read()
    print(out)
    print "Internet Explorer cache is cleared"
    
except:
    pass
