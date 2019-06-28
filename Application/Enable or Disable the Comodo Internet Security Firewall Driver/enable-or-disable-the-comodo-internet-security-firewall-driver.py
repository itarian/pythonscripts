State =itsm.getParameter('Enter_the_state')## Here mention the status enable or disable to change firewall state

import os
import platform
import ssl
def Download(src_path, URL,fp):
    import urllib2
    
    request = urllib2.Request(URL, headers={'User-Agent' : "Magic Browser"})
    try:
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        parsed = urllib2.urlopen(request,context=gcontext)
    except:
        parsed = urllib2.urlopen(request)
    if not os.path.exists(src_path):
        os.makedirs(src_path)
    with open(fp, 'wb') as f:
        while True:
            chunk=parsed.read(100*1000*1000)
            if chunk:
                f.write(chunk)
            else:
                break
    return fp

def os_platform():
    true_platform = os.environ['PROCESSOR_ARCHITECTURE']
    try:
            true_platform = os.environ["PROCESSOR_ARCHITEW6432"]
    except KeyError:
            pass
            #true_platform not assigned to if this does not exist
    return true_platform

Folder=os.environ['programdata']+r"\Noproblem"
if not os.path.exists(Folder):
    os.mkdir(Folder)
fileName=r"nvspbind.exe"
src_path=Folder
fp = os.path.join(src_path, fileName)    
ki=os_platform()
archi=int(filter(str.isdigit, ki))
URL64=r"https://docs.google.com/uc?export=download&id=1q6fZRPsIc_PlLlkR_hUtjZC-eijLrbPU"
URL32=r"https://docs.google.com/uc?export=download&id=15axFfpzdQWUkAS9RTvg9am8Ce0K3XToq"
if archi==64:
    Excutable_path=Download(Folder, URL64,fp)
else:
    Excutable_path=Download(Folder, URL32,fp)   
output=Folder+"\\"+"nvspbind.exe"+" >c:\Output.txt"
os.popen(output)
path2=r"c:\Output.txt"
li=[]
count=0
if State == "enable":
    with open(path2,"r") as f:
        for line in f:
            if "inspect" in line:
                li.append(line)
    for i  in range  (0,len(li)):
        if "disabled:" in li[i]:
            count=count+1
            
    if count>=1:
        osver=platform.release()
        if (osver=='7'):
            b=Folder+"\\"+"nvspbind.exe"+' /e "Local Area Connection" inspect'
            a=os.popen(b).read()
            print"Comodo Internet Security Firewall Driver Enabled"
        else:
            b=Folder+"\\"+"nvspbind.exe"+' /e Ethernet inspect'
            for i in range(0,1):
                a=os.popen(b).read()
            print"Comodo Internet Security Firewall Driver Enabled"
    elif count == 0:
        with open(path2,"r") as f:
            for line in f:
                if "cesfw" in line:
                    li.append(line)
        for i  in range  (0,len(li)):
            if "disabled:" in li[i]:
                count=count+1
                
        if count>=1:
            osver=platform.release()
            if (osver=='7'):
                b=Folder+"\\"+"nvspbind.exe"+' /e "Local Area Connection" cesfw'
                a=os.popen(b).read()
                print"Comodo Internet Security Firewall Driver Enabled"
            else:
                b=Folder+"\\"+"nvspbind.exe"+' /e Ethernet cesfw'
                a=os.popen(b).read()
                print"Comodo Internet Security Firewall Driver Enabled"
        else:
            print"Comodo Internet Security Firewall Driver Already Enabled"

    Folder=os.environ['programdata']+r"\Noproblem"
    try:
        shutil.rmtree(Folder)
    except:
        pass
                
    path2=r"c:\Output.txt"
    try:
        os.remove(path2)
    except:
        pass
else:
    with open(path2,"r") as f:
        for line in f:
            if "inspect" in line:
                li.append(line)
    for i  in range  (0,len(li)):
        if "enabled:" in li[i]:
            count=count+1        
    if count>=1:
        osver=platform.release()
        if (osver=='7'):
            b=Folder+"\\"+"nvspbind.exe"+' /d "Local Area Connection" inspect'
            a=os.popen(b).read()
            print"Comodo Internet Security Firewall Driver disabled"
        else:
            b=Folder+"\\"+"nvspbind.exe"+' /d Ethernet inspect'
            for i in range(0,1):
                a=os.popen(b).read()
            print"Comodo Internet Security Firewall Driver disabled"
    elif count == 0:
        with open(path2,"r") as f:
            for line in f:
                if "cesfw" in line:
                    li.append(line)
        for i  in range  (0,len(li)):
            if "enabled:" in li[i]:
                count=count+1        
        if count>=1:
            osver=platform.release()
            if (osver=='7'):
                b=Folder+"\\"+"nvspbind.exe"+' /d "Local Area Connection" cesfw'
                a=os.popen(b).read()
                print"Comodo Internet Security Firewall Driver disabled"
            else:
                b=Folder+"\\"+"nvspbind.exe"+' /d Ethernet cesfw'
                for i in range(0,1):
                    a=os.popen(b).read()
                print"Comodo Internet Security Firewall Driver disabled"
        else:
            print"Comodo Internet Security Firewall Driver Already disabled"

    Folder=os.environ['programdata']+r"\Noproblem"
    try:
        shutil.rmtree(Folder)
    except:
        pass
                
    path2=r"c:\Output.txt"
    try:
        os.remove(path2)
    except:
        pass
