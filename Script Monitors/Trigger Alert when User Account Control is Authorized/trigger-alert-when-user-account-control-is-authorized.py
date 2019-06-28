# The script is a template to check UAC status on device.
import os
import sys
import _winreg

def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))

# Please use "alert(1)" to turn on the monitor(trigger an alert)
# Please use "alert(0)" to turn off the monitor(disable an alert)
# Please do not change above block and write your script below
def UAC_CONTROLL():
    import os
    import re
    import sys
    import xml.etree.ElementTree as ET
    import getpass
    import socket
    print "USER NAME: "+getpass.getuser()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print "IP-ADDRESS : "+(s.getsockname()[0])
    from time import gmtime, strftime
    time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print '\n'
    event_logs=os.popen('wevtutil qe Security /f:text /c:20 /rd:True ').read()
    reg_log=re.findall('Event\sID:\s46[0-9]{2}',event_logs)
    get_reg,ale=0,0
    get_reg1=0
    get_reg2=0
    for id in reg_log:
        if id=='Event ID: 4672':
            get_reg=get_reg+1
        elif id=='Event ID: 4624':
            get_reg1=get_reg1+1
        elif id=='Event ID: 4648':
            get_reg2=get_reg2+1


    if get_reg>0:
        print '1: UAC AUTHOURIZED TO THE LOGON USER'
        event_logs1=os.popen('wevtutil qe Security /f:xml /c:20 /rd:True |findstr ="Event ID: 4672"').read()
        k=re.search('<System>.*<?System>',event_logs1)
        k=k.group()
        print '\n'
        print 'Here are the following details with EVENT ID :'
        print '\n'
        xml = ET.fromstring(k)
        for i in xml.getchildren():
            if i.attrib != {}:
                print i.tag, i.attrib
            else:
                if i.text is not None:
                    print i.tag, i.text
                     
        ale=ale+1
             
    else:
            print '\n'
            print '1: NO, "UAC AUTHOURIZED TO THE LOGON USER"'
             

     

    if get_reg1>0:
            print '2: A new process has been created/recorded in the audit process tracking'
            event_logs2=os.popen('wevtutil qe Security /f:xml /c:20 /rd:True |findstr ="Event ID: 4624"').read()
            k=re.search('<System>.*<?System>',event_logs2)
            k=k.group()
            print '\n'
            print 'Here are the following  Audit Process Tracking details with  coressponding EVENT ID :'
            print '\n'
            xml = ET.fromstring(k)
            for i in xml.getchildren():
                if i.attrib != {}:
                        print i.tag, i.attrib
                else:
                    if i.text is not None:
                        print i.tag, i.text

            ale=ale+1 
    else:
            print '\n'
            print '2: NO, "A new process has been created/recorded in the audit process tracking"'
            print '\n'
             

         
    if get_reg2>0:
        print '3: Usage of user account with admin rights'
        event_logs3=os.popen('wevtutil qe Security /f:xml /c:20 /rd:True |findstr ="Event ID: 4648"').read()
        k=re.search('<System>.*<?System>',event_logs3)
        k=k.group()
        print '\n'
        print 'Here are the following details with EVENT ID :'
        print '\n'
        xml = ET.fromstring(k)
        for i in xml.getchildren():
            if i.attrib != {}:
                print i.tag, i.attrib
            else:
                if i.text is not None:
                    print i.tag, i.text
        ale=ale+1
     
    else:
            print '\n'
            print '3: NO,"Usage of user account with admin rights"'
    if ale>0:
        alert(1)
    else :
        alert(0)

             




UAC_CONTROLL()
