# The script is a template to check UAC status on device.
import os
import sys
import _winreg

def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))

# Please use "alert(1)" to turn on the monitor(trigger an alert)
# Please use "alert(0)" to turn off the monitor(disable an alert)
# Please do not change above block and write your script below
def admin_accesses():
    import os
    import re
    import getpass
    import socket
    print "USER NAME: "+getpass.getuser()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print "IP-ADDRESS : "+(s.getsockname()[0])
    from time import gmtime, strftime
    time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    #logon attempt
    event_logs1=os.popen('wevtutil qe Security /f:text /c:5000 /rd:True').read()
    reg_log=re.findall('Event\sID:\s[0-9]{4}',event_logs1)
    get_reg1=0
    for id in reg_log:
        if id=='Event ID: 528':
            get_reg1=get_reg1+1
        elif id=='Event ID: 4624':
            get_reg1=get_reg1+1
        elif id=='Event ID: 4672':
            get_reg1=get_reg1+1


    #LOGOFF
    event_logs2=os.popen('wevtutil qe Security /f:text /c:5000 /rd:True').read()
    reg_log=re.findall('Event\sID:\s[0-9]{4}',event_logs2)
    get_reg2=0
    for id in reg_log:
        if id=='Event ID: 538':
            get_reg2=get_reg2+1
        elif id=='Event ID: 4634':
            get_reg2=get_reg2+1
        elif id=='Event ID: 4647':
            get_reg2=get_reg2+1


    #logon failure atttempt
    event_logs3=os.popen('wevtutil qe Security /f:text /c:5000 /rd:True').read()
    reg_log=re.findall('Event\sID:\s[0-9]{4}',event_logs3)
    get_reg3=0
    for id in reg_log:
        if id=='Event ID: 537':
            get_reg3=get_reg3+1
        elif id=='Event ID: 4625':
            get_reg3=get_reg3+1


    if get_reg1 > 0:
        alert(1)
        print '\nA LOGON ATTEMPT WAS MADE IN YOUR SYSTEM'
    elif get_reg2 > 0:
        alert(1)
        print '\nA LOGOFF ATTEMPT WAS MADE IN YOUR SYSTEM'
    elif get_reg3 > 0:
        alert(1)
        print'\nUNABLE TO LOGON\A LOGON FAILURE WAS MADE IN YOUR SYSTEM'
    else:
        alert(0)
        print '\nNo Logon, Logoff and Logon Failure was happened'
admin_accesses()
