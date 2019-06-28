# The script is a template to check UAC status on device.
import os
import sys
def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))
# Please use "alert(1)" to turn on the monitor(trigger an alert)
# Please use "alert(0)" to turn off the monitor(disable an alert)
# Please do not change above block and write your script below
def password_changed():
    import re
    import os
    import getpass
    import socket
    print "USER NAME: "+getpass.getuser()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print "IP-ADDRESS : "+(s.getsockname()[0])
    from time import gmtime, strftime
    time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    event_logs=os.popen('wevtutil qe Security /f:text /c:2000 /rd:True').read()
    reg_log=re.findall('Event\sID:\s47[0-9]{2}',event_logs)
    get_reg=0
    for id in reg_log:
        if id=='Event ID: 4723':
            get_reg=get_reg+1
        elif id=='Event ID: 627':
            get_reg=get_reg+1


    if get_reg>0:
        print time+" :  YOUR SYSTEM PASSWORD HAS BEEN CHANGED"
        alert(1)
    else:
        print time+" :  YOUR SYSTEM PASSWORD REMAINS SAME"
        alert(0)
password_changed()
