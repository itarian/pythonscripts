Website_url = r"www.google.com" #Give your Website url without https/http
preferred_speed=750   #Give your website performance value in milliseconds. 


import os 
import sys 
import _winreg
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

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg)) 

# Please use "alert(1)" to turn on the monitor(trigger an alert) 
# Please use "alert(0)" to turn off the monitor(disable an alert) 
# Please do not change above block and write your script below 

def speed(cmd):
    import os
    s=[]
    for i in [i.strip() for i in cmd if i.strip()]:
        s.append(i)
    b=(''.join(s))
    index_range=b.index('Average=')
    index_range+=8
    f=[]
    for i in range(index_range,len(b)):
        g=b[i]
        f.append(g)
    average_speed=(''.join(f))
    d=average_speed.strip('ms')
    int_val=int(d)  
    return int_val


with disable_file_system_redirection():
    cmd=os.popen("ping -n 3 "+Website_url).read()
    try:
        if "Ping request could not find host" in cmd:
            print "ERROR - Please check the Website's Url or IP address........."
            alert(1)
        elif "Request timed out." in cmd:      
            print "ERROR - Please check the Connection or Website's Url........"
            alert(1)                 
        elif "Approximate round trip times in milli-seconds:" in cmd:
            sp=speed(cmd)
            if sp<preferred_speed:
                print "Success!! - Website maintains the %dms speed limit........."% (preferred_speed)
                alert(0)
            else:
                print "Issue - Website doesn't maintains the %dms speed limit........."% (preferred_speed)
                alert(1)
        else:
            try:
                sp=speed(cmd)
                if sp<preferred_speed:
                    print "Success!! - Website maintains the %dms speed limit........."% (preferred_speed)
                    alert(0)
                else:
                    print "Issue - Website doesn't maintains the %dms speed limit........."% (preferred_speed)
                    alert(1)
            except Exception as err: 
                print "Failed due to the below error"
                print err
                alert(1)
    except Exception as err: 
            print "Failed due to the below error"
            print err
            alert(1)
