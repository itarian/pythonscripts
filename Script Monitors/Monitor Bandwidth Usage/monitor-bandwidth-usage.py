Sizenumber=10
SizeDef="MB"   #KB or MB or GB      #SizeDef is case sensitive it should be declared in caps letters
import os
import ctypes
import re
import math
import sys
ps_content=r'''
Get-NetAdapterStatistics
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
def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))
def ecmd(command):
    import ctypes
    from subprocess import PIPE, Popen

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
def convert_size(B):
   'Return the given bytes as a human friendly KB, MB, GB, or TB string'
   B = float(B)
   KB = float(1024)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)
def parseSize(size):
    units = {"Byte": 1, "KB": 10**3, "MB": 10**6, "GB": 10**9, "TB": 10**12}
    number, unit = [string.strip() for string in size.split()]
    return int(float(number)*units[unit])

def bandwidth():
    file_name='powershell_file.ps1'
    file_path=os.path.join(os.environ['TEMP'], file_name)
    with open(file_path, 'wb') as wr:
        wr.write(ps_content)
    ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
    ki=ecmd('powershell "%s"'%file_path)
    ki=str(ki)
    import re
    sam=re.findall('Ethernet(.*)',ki)
    os.remove(file_path)
    if sam>0:
        sam1=re.sub(' +',' ',sam[0])
        sam1=sam1.replace(" ",",")
        sam1=sam1.split(",")
        return sam1[1]
def comparision(Sizenumber,SizeDef,data):
    num=re.findall("Received Bytes: (.*)",data)[0]
    num=int(num)
    num=convert_size(num)
    num=parseSize(num)
    convert=(int(output))
    convert=convert_size(convert)
    convert=parseSize(convert)
    ki=parseSize(str(Sizenumber)+" "+SizeDef)
    Total=convert-num
    Total=abs(Total)
    if Total>ki:
        print "You accessed more data"
        print "You have used "+str(convert_size(Total))
        ale=1
        return ale
    else:
        print "You are using limited data"
        print "You have used "+str(convert_size(Total))
        ale=0
        return ale
path=os.path.join(os.environ['programdata'],"temp","Bandwidth.txt")
if os.path.exists(path):
    output=bandwidth()
    with open(path,"r")as f:
        data=f.read()
    ale=comparision(Sizenumber,SizeDef,data)
    with open(path,"w+")as f:
        f.write("Received Bytes: " + output)   
else:
    try:
        os.mkdir(os.path.join(os.environ['programdata'],"temp"))
    except:
        pass
    output=bandwidth()
    with open(path,"w")as f:
        f.write("Received Bytes: " + output)
    ale=0
    print "Script is running for first time"

if ale==1:
    alert(1)
else:
    alert(0)
