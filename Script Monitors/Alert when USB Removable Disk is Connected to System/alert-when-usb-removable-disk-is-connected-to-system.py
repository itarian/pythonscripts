# The script is a template to check UAC status on device.
import os
import sys

def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))
def ExecuteCMD(CMD, OUT = False):
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
    from subprocess import PIPE, Popen
    with disable_file_system_redirection():
        OBJ = Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = OBJ.communicate()
    return out
def check(ale):
    CMD='REG query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Enum\USBSTOR"'
    out=ExecuteCMD(CMD, OUT = False)
    out=out.replace("\r","")
    out=out.split('\n')
    output=[]
    for i in out:
        ki=os.path.basename(i)
        ki=ki.replace("Disk&Ven_","")
        ki.replace("&Rev_1.00","")
        ki=ki.replace("&Rev_1.00","")
        USBNAME=ki.replace("&Prod_","_")
        output.append(USBNAME)
        output.append("|")
    output1="".join(output)
    PROGRAMDATA=os.environ['programdata']
    COMP_PATH=os.path.join(PROGRAMDATA,"Compare_usb.txt")
    if os.path.exists(COMP_PATH):
        with open(COMP_PATH,"r") as f:
            ki=f.read()
            if ale==0:
                ki=ki.split('\n')
                for i in ki:
                    if len(i)>1:
                        if i=="||":
                            z=1
                        else:
                            print i+"  Devices is added in endpoint before 1 Min"
                            for i in out:
                                C='REG DELETE "'+i+'" /F'
                                ExecuteCMD(C, OUT = False)
                                z=0
                           
            else:
                for i in output:
                    if len(i)>2:
                        print i+"  Devices is detected on endpoint"
                        
        COMP_PATH=r"C:/ProgramData/Compare_usb.txt"
        os.remove(COMP_PATH)
        if z==0:
            return 0
        
                
            
    else:
        
        with open(COMP_PATH,"w") as f:
            f.write(output1)
    
    
def USB():
    import os
    import sys
    import getpass
    print "USER NAME: "+getpass.getuser()
    import re
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print "IP-ADDRESS : "+(s.getsockname()[0])
    a=os.popen('wmic logicaldisk where drivetype=2 get deviceid, volumename, description,size').read()
    dev=re.findall('([A-Z]:\s+[0-9]+|[A-Z]:\s+)',a)
    list=[]
    ki=1
    for i in dev:
        list.append(i.split())
    ale=0
    length=len(list)
    if length==1:
        ale=0
        ki=check(ale)
    else:
        for i in list:
            try:
                if len(i[1])>0:
                    print i[0] +" New USB REMOVABLE DEVICE(S) HAS BEEN DETECTED BY YOUR SYSTEM"
                    ale=ale+1
                else:
                    ale=0
                    ki=check(ale)
            except:
                pass
            
    
    if ki==0:
        alert(1)
    else:
        if ale>0:
            alert(1)
        else:
            print "NO NEW DEVICES DETECTED"
            alert(0)
                

USB()
