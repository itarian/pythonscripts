dlist='"fitsmallbusiness.com","businessnewsdaily.com","techradar.com"' #please enter the domain name for which you need to monitor domain expiry date

#For example pass domain name like this "flypaper.com","techradar.com"

ps_content=r'''
    [String] $list
    [String] $urlnames

    Function WhoIs {
    $domains=@(%s)
    foreach ($domain in $domains)  
    { 
         Write-Host "Connecting to Web Services URL..." -ForegroundColor Green
    try {
    #Retrieve the data from web service WSDL
    If ($whois = New-WebServiceProxy -uri "http://www.webservicex.net/whois.asmx?WSDL") {Write-Host "Ok" -ForegroundColor Green}
    else {Write-Host "Error" -ForegroundColor Red}
    Write-Host "Gathering $domain data..." -ForegroundColor Green
    #Return the data
    (($whois.getwhois("=$domain")).Split("<<<")[0])
    } catch {
    Write-Host "www.microsoft.com" -ForegroundColor Red}
    } #end function WhoIs
    }
            
    WhoIs


'''%dlist
import _winreg 
import os
import re
import socket
import sys
global count
count =0
def alert(arg):
  sys.stderr.write("%d%d%d" % (arg, arg, arg))
def information():
  name=os.environ['username']
  print 'PC-NAME : '+name
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
   
  print "IP-ADDRESS : " + (s.getsockname()[0])
  path="c:\windows\system32"
  os.chdir(path)
  out=os.popen("cscript slmgr.vbs -dli").read()
  c=0
  os.environ
  k,li,up,no,no1=[],[],[],[],[]
   
  ab=re.findall('Licensed',out)
  bc=re.findall('([0-9]{2}\sday.*)',out)
  cd=re.findall('0xC004F056',out)
  de=re.findall('0xC004F034',out)
  lea=len(ab)
  leb=len(bc)
  lec=len(cd)
  led=len(de)
  for i in ab:
      li.append(i)
  for j in bc:
      up.append(j)
  for k in cd:
      no.append(k)
  for l in de:
      no1.append(l)
  if  lea!=0:
      if ab==li:
          print "Your windows is Activated."
          count=0
  if leb!=0:
      if bc==up:
          up.append('Left to expire your windows,Please Activate it.')
          str1=''.join(str(e)for e in up)
          print str1
          count=+1
  if lec!=0:
      if cd==no:
          print "You need to Activate your windows."
          count=+1
  if led!=0:
      if de==no1:
          print "you need to Activate your windows."
          count=+1
  try:
     return count
  except:
      pass

count=information()

import os
import re
import datetime
import sys
vblines= ps_content 
temp=os.environ['TEMP']
path=temp+'\\powershell_file.ps1'

files=open(path,'w+')
files.write(ps_content)
files.close()

count1=0
def ecmd(command):
    import ctypes
    from subprocess import PIPE, Popen
    
    class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
    
    with disable_file_system_redirection():
        obj = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()
    ret=obj.returncode
    if ret==0:
        if out:
            return out.strip()
        else:
            return ret
    else:
        if err:
            return err.strip()
        else:
            return ret

file_name='powershell_file.ps1'
file_path=os.path.join(os.environ['TEMP'], file_name)
with open(file_path, 'wb') as wr:
    wr.write(ps_content)

ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
a=ecmd('powershell "%s"'%file_path)



b=re.findall('Registry\sExpiry\sDate:(.*)T',a)
today = datetime.date.today()

c=re.findall('Domain Name:(.*)',a)



dct = dict(zip(c, b))

i=0
count1=0
for value in dct.values():
    selected_month_rec = value
    date_formate = datetime.date(int(selected_month_rec.split('-')[0]),int(selected_month_rec.split('-')[1]),int(selected_month_rec.split('-')[2]))
    v=date_formate
    today = datetime.date.today()
    ins = v - today
    inst=str(ins)
    
    t=re.findall('(.*)days',inst)
    t=int(t[0])
    m=t-1810
    if(m<10):
        print dct.keys()[i]+" domain is expiring in few days"
        count1=+1
        i=i+1
        
if count>0 or count1>0:
    alert(1)
else:
    alert(0)
    
os.remove(file_path)
