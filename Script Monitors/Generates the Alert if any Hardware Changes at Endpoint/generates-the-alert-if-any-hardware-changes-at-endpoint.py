import os 
import sys 
import _winreg 

def alert(arg): 
    sys.stderr.write("%d%d%d" % (arg, arg, arg)) 

import os,sys,_winreg,re,socket,difflib,filecmp
fnd=0
fnd1=0
val=0
val1=0
workdir=os.environ['PROGRAMDATA']+r'\c1_temp'
if not os.path.isdir(workdir):
    os.mkdir(workdir)
    
path="C:\ProgramData\c1_temp\TEST.txt"
path2="C:\ProgramData\c1_temp\TEST2.txt"
fnd=0
def files():
    file_name = "TEST.txt"
    cur_dir = "C:\ProgramData\c1_temp"
    file_list = os.listdir(cur_dir)
    parent_dir = os.path.dirname(cur_dir)
    if file_name in file_list:
        global fnd
        fnd=1
    else:
        print "File not found"
        global fnd1
        fnd1=1

def computername():
    import os
    print "Computer Name :"
    print  os.environ['COMPUTERNAME']

def ipaddress():
    import socket
    print "IP-Address :"
    print  socket.gethostbyname(socket.gethostname())

def EXCUTE():
    if fnd==1:
        File2=open(path2,"w+")
    elif fnd1==1:
        File1=open(path,"w+")
    import ctypes
    class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
    disable_file_system_redirection()
    samout="SYSTEM INFORMATION "
    out=os.popen('systeminfo.exe').read()
    samout1="PRINTER INFORMATION"
    out1=os.popen('powershell Get-Ciminstance WIn32_Printer ').read()
    samout2="NETWORK ADAPTER"
    out2=os.popen('powershell Get-Ciminstance  Win32_NetworkAdapterConfiguration  ').read()
    samout3="ONBOARD DEVICE DETAILS"
    out3=os.popen('powershell Get-WmiObject Win32_baseboard ').read()
    output=samout+out+samout1+out1+samout2+out2+samout3+out3
    if fnd==1:
        File2.write(output)
    elif fnd1==1:
        File1.write(output)
def swchanges():
    list1=[]
    ale=0
    if fnd1==1:
        alert(0)
        return
    v=filecmp.cmp(path,path2)
    with open(path) as file:
        data=file.read()
    with open(path2) as file:
        data2=file.read()
    text1Lines = data.splitlines(1)
    text2Lines = data2.splitlines(1)  
    diffInstance = difflib.Differ()
    diffList = list(diffInstance.compare(text2Lines, text1Lines))
    for line in diffList:
        if '- Virtual Memory: Available:' in line :
            continue
        elif 'Available Physical Memory:' in line :
            continue
        elif 'Virtual Memory: In Use:' in line :
            continue
        elif ' Intel64 Family 6 Model 94 Stepping' in line:
            continue
        elif line[0]=='-':
            print "Changes in:"
            print line
            print "*******"
            ale=ale+1
            print data2
    if ale==0:
        print "\n"
        print "NO Hardware changes\n"
        print "*******"
        print "\n"
        print data2
        alert(0)
    elif ale>0:
        alert(1)
    os.remove(path2)

computername()
ipaddress()
files()
EXCUTE()
swchanges()
