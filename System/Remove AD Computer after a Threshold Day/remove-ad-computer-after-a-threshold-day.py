#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('parameterName') with that parameter's name
rem_value='30' # Provide the days to remove the account

import sys
import os

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg))
   
ps_content=r'''
Import-Module ActiveDirectory
get-adComputer -Filter * -Properties *  | Sort LastLogonDate | FT Name, LastLogonDate -Autosize
'''

ps_content_1=r'''
Import-Module ActiveDirectory
get-adComputer -Filter * -Properties *  | Sort LastLogonDate | FT LastLogonDate -Autosize
'''

hn_name=os.popen('hostname').read()

import re
from datetime import date, timedelta
import datetime
from datetime import datetime
from datetime import datetime, date, time
from datetime import datetime, date, time
import os
import time
import ctypes
import subprocess
from datetime import datetime

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

file_name='powershell_file_4.ps1'
file_path=os.path.join(os.environ['TEMP'], file_name)
with open(file_path, 'wb') as wr:
    wr.write(ps_content)

file_name_1='powershell_file_5.ps1'
file_path_1=os.path.join(os.environ['TEMP'], file_name_1)
with open(file_path_1, 'wb') as wr:
    wr.write(ps_content_1)

ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
a=ecmd('powershell "%s"'%file_path)
b=ecmd('powershell "%s"'%file_path_1)

def check():
   ps_content_2='powershell "Get-ADComputer -Filter * -Property Enabled | FT Name,Enabled -Autosize"'
   ping = os.popen(ps_content_2).read()
   return ping

ping=check()

def get_date(dateFormat="%m/%d/%Y"):
    import datetime
    timeNow = datetime.datetime.now()
    anotherTime_1 = timeNow - datetime.timedelta(days=int(rem_value))
    return anotherTime_1.strftime(dateFormat)

output_format = '%m/%d/%Y'
rm_time=get_date(output_format)

s=[]
y=[]
val=[]
val1=[]
y1=[]
w=[]
value=[]
r=[]
y2=[]

def recheck1():
   for i in [i.strip() for i in a.split('\r\n')  if i.strip()]:
      s.append(i)

   a1=s[2:]
   return a1

def recheck2():
   for i in [i.strip() for i in b.split('\r\n')  if i.strip()]:
      y.append(i)
   b1=y[2:]
   return b1

def recheck3():
   for i in [i.strip() for i in ping.split('\n')  if i.strip()]:
      w.append(i)
   r1=w[2:]

   return r1

a1=recheck1()
b1=recheck2()
r1=recheck3()

for j in b1:
    xy=[x.strip() for x in j.split(',')]
    for z in xy:
        if re.findall('(.*)AM',z):
            v=z
        elif re.findall('(.*)PM',z):
            v=z
        else:
            v=''
        if v == '':
            pass
        else:
            val.append(v)
        
for i in a1:
    xz=[x.strip() for x in i.split(',')]
    for zy in xz:
        if re.findall('(.*)AM',zy):
            v1=zy
        elif re.findall('(.*)PM',zy):
            v1=zy
        else:
            v1=''
            pass
        if v1 == '':
            pass
        else:
            val1.append(v1)

for k in val and val1:
   xx=k.split()[1]
   xx=xx.strip()
   tt = datetime.strptime(xx,'%m/%d/%Y')
   tt1 = datetime.strptime(rm_time,'%m/%d/%Y')
   if tt1 > tt:
      if hn_name in k:
         pass

      else:
         k2=k.split()[0]
         y1.append(k2)


for j in range(0,len(y1)):
    ps_content_2=r'powershell "Remove-ADobject (Get-ADComputer %s).distinguishedname -Recursive -Confirm:$false"'%y1[j]
    ping = subprocess.Popen(ps_content_2,stdout=subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
    out=ping.communicate()[0]
    output = str(out)            
    try:
        os.remove(file_path)
    except:
        pass

    try:
        os.remove(file_path_1)
    except:
        pass

if y1:
    print "Removed computers successfully..."
    
    
