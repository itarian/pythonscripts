kayako_ticket_number="GOI-221-286602"
import os,sys,csv,urllib2,zipfile,shutil,re,sys,socket,_winreg,random,getpass,time
import xml.etree.ElementTree as ET
from subprocess import PIPE, Popen
a=[]
b=[]
c=[]
import io
print "USER NAME: "+getpass.getuser()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
computer_name=os.getenv('computername')
time_tag=time.strftime('%Y_%m_%d_%H_%M_%S')
file_name='%s_CustomerReport_%s_%s.zip'%(kayako_ticket_number, computer_name, time_tag)
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
def csvedit(str23):
    list=[]
    li=[]
    for i,c in enumerate(str23):
        if ":"==c:
            li.append(i)
        

    if len(li)>0:
        for i in range(1,len(li)):
            
            str23=  str23[:li[i]]+'\n'+ str23[li[i]+1:]
        return str23
def Systeminfo():
    
    a.append("\\nSYSTEM INFO\\n")
    ki=os.popen('systeminfo').read()
    space=ki.replace(r' ','')
    space1=space.split('\n')
    for j in space1:
        sam=j
        a.append(csvedit(sam))
    global str1
    str1= '\n'.join(str(e) for e in a)
    
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
                    ki="\n"+inlist[0]+" "+inlist[1]+"\n"
                    b.append(ki)
                    global str2
                    str2 = ''.join(str(e) for e in b)
            except:
                pass
            i+=1
        except:
            break
    _winreg.CloseKey(oK)

def sftp_transfer(winscp_program_path, script_path, file_to_send):
    script_code=r"""
open sftp://c1report:paT7rObeseW0duLl@c1report.comodo.com/ -hostkey=*
cd /reports
put "%s"
close
exit
"""%file_to_send
    with open(script_path, "w") as writer:
        writer.write(script_code)
    transfer_object=Popen('"%s" /script="%s"'%(winscp_program_path, script_path), shell=True, stdout=PIPE, stderr=PIPE)
    transfer_object.communicate()
    return transfer_object.returncode
def zip_item(path, zip_file_path):
    
    
    zip_object=zipfile.ZipFile(zip_file_path, 'w')
    
    from subprocess import Popen, PIPE, call

    
    if os.path.isfile(path):
        try:
            os.chmod(path,0644)
        except:
            pass
        zip_object.write(path, path.split(os.sep)[-1])
        zip_object.close()
        return zip_file_path
    else:
        length_directory_path=len(path)
        for root, directories, files in os.walk(path):
            for file_name in files:
                try:
                    os.chmod(file_name,0644)
                except:
                    pass
                file_path=os.path.join(root, file_name) 
                zip_object.write(file_path, file_path[length_directory_path:])
        zip_object.close()
        return zip_file_path
    
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

def download(url, file_path):
    url_object=urllib2.urlopen(url)
    download_data=url_object.read()
    with open(file_path, "wb") as writer:
        writer.write(download_data)
    return file_path

def ecmd(CMD):
    import ctypes
    CMD="wmic "+ CMD +" LIST brief"
    class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
    from subprocess import PIPE, Popen
    with disable_file_system_redirection():
        OBJ = Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = OBJ.communicate()
    return out.strip()

Systeminfo()
INST=("\n INSTALLED SOFTWARE  LIST \n")
programsinstalled()

temp=os.environ['TEMP']
Af=os.path.join(temp, "Customer_report_%s"%time_tag)
os.mkdir(Af)

Bf=Af+"\SYSTEMINFO.txt"
with open(Bf, "w") as myfile:
    myfile.write("\n")
    myfile.write("%s\n" % str1)
    myfile.close()
    
Cf=Af+"\INSTALLED_SOFTWARES.txt"
with open(Cf, "w") as myfile:
    myfile.write(INST)
    myfile.write("%s\n" % str2)
    myfile.close()
    
checkhardware=["BASEBOARD","BIOS","CDROM","COMPUTERSYSTEM","CPU","CSProduct","DESKTOP","DISKDRIVE","ENVIRONMENT","GROUP","IDECONTROLLER","NETPROTOCOL","OS","PRINTER","SYSTEMSLOT",]
Df=Af+"\HARDWARE_DETAILS.txt"
with open(Df, "w") as myfile:
    for i in checkhardware:
        myfile.write(r"*************")
        myfile.write("\n")
        myfile.write ("\n"+i+" Brief\n")
        myfile.write("\n")
        myfile.write("\n"+r"*************"+"\n")
        myfile.write(ecmd(i))
Ef=Af+"\Permissions.cfg"
Permissions="secedit /export /areas USER_RIGHTS /cfg %s"%(Ef)
os.popen(Permissions).read()
Ff=Af+"\FirewallRules.txt"
Firewall="netsh advfirewall firewall show rule name=all dir=in type=dynamic  >%s"%(Ff)
os.popen(Firewall).read()
Gf=Af+"\DomainsUsers.txt"
Users="WMIC USERACCOUNT LIST BRIEF >%s"%(Gf)
os.popen(Users).read()
Hf=Af+"\Services.txt"
Services="sc queryex type= service state= all >%s"%(Hf)
os.popen(Services).read()

path=Af
file_name=temp+"\\"+file_name
zip1=zip_item(path,file_name)

temp_folder='temp_logs'
work_directory=os.path.join(os.getenv('temp'), temp_folder)
if os.path.isdir(work_directory):
    shutil.rmtree(work_directory)
os.mkdir(work_directory)
winscp_file_path=os.path.join(work_directory, 'WinSCP_C1_SFTP.exe')
winscp_url="https://patchportal.one.comodo.com/portal/packages/spm/DYMO%20Label%20Software/x86/WinSCP.exe"
winscp_program_path=download(winscp_url, winscp_file_path)
winscp_script_file=os.path.join(work_directory, 'script_winscp.txt')

if sftp_transfer(winscp_program_path, winscp_script_file, zip1)==0:
    print 'Transfering Customer Environment Report %s Done'%('.'*15)
   
else:
    print 'Failed to Transfer Customer Environment Report'
if os.path.isdir(work_directory):
    shutil.rmtree(work_directory)
try :
    shutil.rmtree(zip1)
except:
    pass
try :
    os.remove(zip1)
except:
    pass
try :
    shutil.rmtree(path)
except:
    pass
try :
    os.remove(path)
except:
    pass
