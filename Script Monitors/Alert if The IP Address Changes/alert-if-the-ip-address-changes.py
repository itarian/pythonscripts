import os 
import sys 
import _winreg 

def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg)) 

# Please use "alert(1)" to turn on the monitor(trigger an alert) 
# Please use "alert(0)" to turn off the monitor(disable an alert) 
# Please do not change above block and write your script below 

import os
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

with disable_file_system_redirection():
    #Declare the file path
    temp = os.environ['PROGRAMDATA']+"\\c1_temp"
    os.chdir(os.environ['PROGRAMDATA'])
    if os.path.exists(temp):
         path = temp +"\\"+"ipchange.txt"
    else:
        os.mkdir("c1_temp")
        path = temp +"\\"+"ipchange.txt"


    #Declare the variable

    count  = 0
    ip_num = []

    #filtering the ip address from output 
    ip = os.popen("ipconfig").read()
    for i in [i.strip() for i in ip.split('\n') if 'IPv4 Address'  in i if i.strip()]:
        s = i
        ip_log = s[36:]
        
    #open and read the file and check for ip address           


    with open(path,"r+") as f:
        for line in f : 
            list01 = [i.strip() for i in line.split('.')  if i.strip()]
            list02 = [i.strip() for i in ip_log.split('.')  if i.strip()]
            campare_list = cmp(list01,list02)
            if campare_list == 0:
                alert(0)
                print "The ip has not changed"
                print "The current ip address is " ,ip_log
            elif campare_list == 1 or campare_list == -1:
                print "The ip address has changed"
                alert(1)
                print "The current ip address is " ,ip_log
                os.chdir(temp)
                if os.path.exists(path):
                    f = open('ipchange.txt', 'r+')
                    f.truncate()

    os.chmod(path,0644)            
    #append the ip to the file 
    with open(path,"a") as f:
        f.write(ip_log +"\n")
