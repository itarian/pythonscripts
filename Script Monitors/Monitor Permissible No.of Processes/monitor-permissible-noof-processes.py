# The script is a template to check UAC status on device.
import os
import sys
import _winreg
pro_count=60

def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))

# Please use "alert(1)" to turn on the monitor(trigger an alert)
# Please use "alert(0)" to turn off the monitor(disable an alert)
# Please do not change above block and write your script below
def process_ki(pro_count):


    import re
    import os,socket,getpass
    name=getpass.getuser()
    print "USER NAME: "+name

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print "IP-ADDRESS: "+(s.getsockname()[0])
    out1=os.popen('tasklist | find /i ".exe" /C').read()
    out=int(out1)
    out2=str(out)
    print out2 +"  Processes Are currently running"
    ram_process=os.popen('tasklist /v /FI "MEMUSAGE ge 10000" | sort /+67 /R').readlines();
    cpu_process=os.popen('tasklist /v /FI "CPUTIME gt 00:03:00" | sort /R /+148').readlines();


    if out>pro_count:
        print"The count limit Exceeded"      
        try:
            print('Top RAM memory consuming processes \n');
            for i in range(1,7,1):
                print (ram_process[i]);
            print('Top cpu consuming processes \n');      
            for i in range(1,7,1):
                print (cpu_process[i])
        except:
            print("Finished");
            alert(1)

    else:
        alert(0)




process_ki(pro_count)
