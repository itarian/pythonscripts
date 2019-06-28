global li
li=["Livedrive.exe"]  #please give exact display name of software
import os
import sys
import _winreg
ale=0
ds=[]
def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))

import re
import socket
def finding_software(name,length):
    c=0
    d=0
    rK = _winreg.HKEY_LOCAL_MACHINE
    sK = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
    openedKey = _winreg.OpenKey(rK, sK, 0, _winreg.KEY_READ)
    arch, bla = _winreg.QueryValueEx(openedKey, 'PROCESSOR_ARCHITECTURE')
    arch = str(arch)
    if arch == 'AMD64':
        sam=os.popen('reg query "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall" /s ').read()
    else:
        sam=os.popen('reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" /s ').read()
    sam1=os.popen('wmic product get ').read()
    reg=re.findall(name,sam)
    reg2=re.findall(name,sam1)
    length=len(reg)
    length2=len(reg2)
    global ale
    ab,bc=0,0
    if reg!=reg2 :
        if len(reg)>0:
                if len(name)==len(reg[0]):
                        print reg[0]+" software is present on End point user"
                        ale=0
        else:
                if len(reg2)==0:
                        print name+"software is not present on your End point user"
                        ale=ale+1
    if len(reg2)>0:
        if len(name)==len(reg2[0]):
            d=d+1
            print reg2[0]+" software is present on End point user"
            bc=bc+1
            ale=0
    else:
        if len(reg)==0:
            print name+" software is not present on your End point usert"
            ale=ale+1

    return ale
		
                      
def giveinformation(i):
    name=i
    length=len(i)
    val=finding_software(name,length)
            
    return val

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
                DV,bla=_winreg.QueryValueEx(oK1,'DisplayVersion')
                inlist=[DN.strip(), DV.strip()]
                if inlist[1]=="None":
                    gh=0
                else:
                    print inlist[0]+" VERSION : "+inlist[1]
            except:
                pass
            i+=1
        except:
            break
    _winreg.CloseKey(oK)
                
def programsinstalled():
    name=os.environ['username']
    print 'PC-NAME : '+name
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print "IP-ADDRESS : " + (s.getsockname()[0])
    print "The softwares which are installed on End point User"
    print"\n"
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
    uninstalled=''
    error=''
    blacklisted=''
    hasnoss=[]
    ic=0
    uc=0
    ec=0
    for i in rklist:
        try:
            col=collectprograms(i[0], i[1], i[2])
            if col ==None:
                No=0
            else:
                print col
        except:
            pass
        
def aler():
    if 1 in [ds[i] for i in range(0,len(ds))]:
        alert(1)
    else :
        alert(0)


programsinstalled()
for i in li:
    sub=giveinformation(i)
    ds.append(sub)
aler()
