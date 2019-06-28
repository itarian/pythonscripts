a=1
set_value=1
#provide value for a based on following:
#set a=0 to print latest 5 error logs
#set a=1 to print all serices on endpoint
#set a=2 to print print all process
#set a=3 to Enable or Disable Network Adapter
#set_value should be 0 or 1, '0' to ENABLE '1' to DISABLE
#set a=4 Enable DHCP
#set a=5 List all available Open ports 

import os
import subprocess
import ctypes
import re
import shutil
vbs1=r'''
strComputer = "." 
Set objWMIService = GetObject("winmgmts:" _ 
    & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2") 
 
Set colNetAdapters = objWMIService.ExecQuery _ 
    ("Select * from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE") 
  
For Each objNetAdapter In colNetAdapters 
    errEnable = objNetAdapter.EnableDHCP() 
Next 
'''
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


if a==0:
    with disable_file_system_redirection():
        syslogs=os.popen('wevtutil qe System "/q:*[System [(Level=2)]]" /f:text /c:5 /rd:True').read()
        print syslogs
elif a==1:
    with disable_file_system_redirection():
        process= subprocess.Popen('wmic service get caption, name, state', shell=True, stdout=subprocess.PIPE)
    result=process.communicate()
    ret=process.returncode
    if ret==0:
        if result[0]:
            print result[0].strip()
        else:
            print result[0]
    else:
        if result[1]:
            print result[1].strip()
        else:
            print result[1]
elif a==2:
    with disable_file_system_redirection():          
        process = subprocess.Popen(['tasklist'],stdout=subprocess.PIPE)
        stdout = process.communicate()[0]
        print 'STDOUT:'
        print stdout
elif a==3:
    print "------Getting Network adapter Details------\n"
    net=os.popen("netsh interface show interface").read()
    print net
    n=re.findall('--\n(.*)', net)
    name=''.join(n)
    na=name.split('  ')[-1]
    print na
    if set_value==0:
        print "Choosen to Enable Network adapter\n"
        get=os.popen("netsh interface set interface "+na+" admin=enable").read()
        print "***NETWORK ENABLED SUCCESSFULLY***"

    else:
        print "Choosen to Disable Network adapter\n"
        print "NOTE: Your System will lost network and automatically Disconnect\n"
        print "***NETWORK DISABLED SUCCESSFULLY***"
        get=os.popen("netsh interface set interface "+na+" admin=disable").read()
    
elif a==4:

    with disable_file_system_redirection():
        cmd=os.popen('ipconfig /all').read()
        a=re.search("DHCP Enabled. . . . . . . . . . . : Yes",cmd)
        if a:
            print "DHCP is already enabled in this interface"
        else:
            workdir=os.environ['PROGRAMDATA']+r'\temp'
            if not os.path.exists(workdir): 
                os.makedirs(workdir)
            with open(workdir+r'\temprun.vbs',"w") as f :
                f.write(vbs1)
            print os.popen('cscript.exe "'+workdir+r'\temprun.vbs"').read()
            print('DHCP .........Enabled')
            if os.path.exists(workdir):
                shutil.rmtree(workdir)
elif a==5:
    print "\nCHECKING THE AVAILABLE PORTS:\n"
    cmd=os.popen("netstat -o -n -a").read()
    print cmd

else:
    print('please ser value to a')

    
    
