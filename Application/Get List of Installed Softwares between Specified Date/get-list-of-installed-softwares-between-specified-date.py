From_date="2018-06-19"   # Enter from date form where you want to check.
To_date="2018-06-21"     # Enter To date upto where it should check. Empty the To_date="" if you don't want to check upto To date.

import os,sys,shutil,re,sys,socket,_winreg,random,getpass

a=[]
b=[]
c=[]
d=[]


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
                DK,bla=_winreg.QueryValueEx(oK1,'InstallDate')
                inlist=[DN.strip(), DV.strip(), DK.strip()]
                if inlist[1]=="None":
                    gh=0
                else:
                    ki="\n"+inlist[0]+" "+inlist[1]+" : "+inlist[2]+"\n"
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
    uninstalled=''
    error=''
    blacklisted=''
    hasnoss=[]
    ic=0
    uc=0
    ec=0
    for i in rklist:
        col=collectprograms(i[0], i[1], i[2])

def check(From_date, To_date):
    From_date=From_date.replace("-","")
    To_date=To_date.replace("-", "")
    start=int(From_date)
    end=int(To_date)
    if start==end:
        return "Please ensure FROM & TO dates are different"
    else:
        for i in sr:
            i=int(i)
            if start < i < end :
                d.append(i)
        return d

def check1(From_date):
    From_date=From_date.replace("-","")
    start=int(From_date)
    for i in sr:
        i=int(i)
        if start < i:
            d.append(i)
    return d

def compare():
    for i in sort:
        i=str(i)
        get=re.findall('(.*): '+i,str2)
    return get
            
    
programsinstalled()

if not str2:
    print "No Installed Softwares on this Endpoint"
else:
    sr=re.findall(':(.*)',str2)

    if not To_date:
        sort=check1(From_date)
        
    else:
        sort=check(From_date, To_date)

    if not sort:
        print "No Softwares has been installed between the entered Dates"
    else:
        jet=compare()
        if not jet :
            print "Couldn't filter the softwares"
        else:
            print "Intalled softwares between given dates are :\n"
            for i in jet:
                print i
                
