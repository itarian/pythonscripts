import os,socket,_winreg,getpass
b=[]
print "USER NAME: "+getpass.getuser()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print "IP-ADDRESS : "+(s.getsockname()[0])
from time import gmtime, strftime
time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
port=587
def computername():
    import os
    return os.environ['COMPUTERNAME']

## get ip address
def ipaddress():
    import socket
    return socket.gethostbyname(socket.gethostname())

def collectprograms(rtkey,pK,kA):
    import _winreg
    import os
    list=[]
    oK=_winreg.OpenKey(rtkey,pK,0,kA)
    i=0
    while True:
        try:
            bkey=_winreg.EnumKey(oK,i)
            vkey=os.path.join(pK,bkey)
            oK1=_winreg.OpenKey(rtkey,vkey,0,kA)
            try:
                DN,bla=_winreg.QueryValueEx(oK1,'DisplayName')
                DV,bla=_winreg.QueryValueEx(oK1,'Publisher')
                DI,bla=_winreg.QueryValueEx(oK1,'InstallDate')
                inlist=[DN.strip(), DV.strip(),DI.strip()]
                if inlist[1]=="None":
                    gh=0
                else:
                    ki="\n"+inlist[0]+" "+inlist[1]+" Date:"+inlist[2]+"\n"
                    b.append(ki)
                    global str2
                    str2 = ''.join(str(e) for e in b)
                                        
            except:
                pass
            i+=1
        except:
            break
    _winreg.CloseKey(oK)

def programsinstalled():
    uninstallkey='SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'
    if 'PROGRAMFILES(X86)' in os.environ.keys():
        rklist=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ),
                (_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ),
                (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ),
                (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ)]
    else:
        rklist=[(_winreg.HKEY_LOCAL_MACHINE,uninstallkey,_winreg.KEY_READ),
                (_winreg.HKEY_CURRENT_USER,uninstallkey,_winreg.KEY_READ)]
    collected=''
    blacklisted=''
    for i in rklist:
        col=collectprograms(i[0], i[1], i[2])
programsinstalled()

ki=re.findall('ESET(.*)',str2)

for i in ki:
    sam=re.findall('Date:(.*)',i)[0]
    d=re.findall('(.*)Date:',i)
    val=('').join(d)
    sam=list(sam)
    sam.insert(4,'/')
    sam.insert(7,'/')   
    strre = ''.join(str(e) for e in sam)
    print 'ESET'+val+'Date: '+strre
    


    

    
