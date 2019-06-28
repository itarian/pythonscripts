import os
import datetime
import re
import subprocess
from subprocess import PIPE, Popen
import sys

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg))
   
tdy=datetime.datetime.today().strftime('%Y-%m-%d')
val=1
try:
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.exists(workdir):
        os.mkdir(workdir)      
except:
    workdir=os.environ['SYTEMDRIVE']
    

print "Checking for Missed events.........\n"
eid=19
cmd="wevtutil qe Microsoft-Windows-Backup /f:text /q:*[System/EventID=%s]   /rd:true /c:1" %(eid)
obj = subprocess.Popen(cmd, shell = True, stdout = PIPE, stderr = PIPE)
out, err = obj.communicate()
if err:
    print err
else:
    d=out
    if d:
        d1=re.findall('Date: (.*)T',d)
        if tdy == d1[0]:
            if not os.path.isfile(os.path.join(workdir, "Missed.txt")):
                with open(os.path.join(workdir, "Missed.txt"), 'w+') as fe:
                    fe.write(str(val))
                print "\t\t*)Backup Missed count: "+str(val)
            else:
                with open(os.path.join(workdir, "Missed.txt"), 'r') as fe:
                    dm=fe.readlines()
                    for i, line in enumerate(dm):
                        if i == 0:
                            dt=val+int(line)
                            with open(os.path.join(workdir, "Missed.txt"), 'w+') as fe:
                                fe.write(str(dt))
                    print "\t\t*)Backup Missed count: "+str(dt)
                    
            des=re.findall('Description:\s*(.*)', d)
            if des[0]:
                print "\n"+des[0]
                alert(1)
            else:
                print "Couldn't retrieve Description for MISSED EVENTS"
        else:
            print "\t\t*)No missed backup actions found.\n"
##############################################################################
##########                   STARTED EVENTS             ######################
##############################################################################
            print "Checking for Started events........\n"
            eid1=1
            cmd="wevtutil qe Microsoft-Windows-Backup /f:text /q:*[System/EventID=%s]   /rd:true /c:1" %(eid1)
            obj = subprocess.Popen(cmd, shell = True, stdout = PIPE, stderr = PIPE)
            out, err = obj.communicate()
            if err:
                print err
            else:
                d2=re.findall('Date: (.*)T',out)
                if tdy == d2[0]:
                    d21=re.findall('T(.*)', out)
                    print "\t\t*)Found a Backup started today at %s. Checking for it's Completed status." %(d21[0])
##############################################################################
##########                   COMPLETED EVENTS             ####################
##############################################################################
                    eid2=14
                    cmd="wevtutil qe Microsoft-Windows-Backup /f:text /q:*[System/EventID=%s]   /rd:true /c:1" %(eid2)
                    obj = subprocess.Popen(cmd, shell = True, stdout = PIPE, stderr = PIPE)
                    out, err = obj.communicate()
                    if err:
                        print err
                    else:
                        d3=re.findall('Date: (.*)T',out)
                        if tdy == d3[0]:
                            d31=re.findall('T(.*)', out)
                            des1=re.findall('Description:\s*(.*)', out)
                            des1[0]=des1[0].replace(".", "")
                            print "\t\t*)"+des1[0]+" at %s. Checking for it's Result." %(d31[0])
##############################################################################
##########                   SUCCESS EVENTS             ######################
##############################################################################
                            eid3=4
                            cmd="wevtutil qe Microsoft-Windows-Backup /f:text /q:*[System/EventID=%s]   /rd:true /c:1" %(eid3)
                            obj = subprocess.Popen(cmd, shell = True, stdout = PIPE, stderr = PIPE)
                            out, err = obj.communicate()
                            if err:
                                print err
                            else:
                                d4=re.findall('Date: (.*)T',out)
                                if tdy == d4[0]:
                                    des2=re.findall('Description:\s*(.*)', out)
                                    print "\t\t*)"+des2[0]
                                    alert(0)
                                else:
##############################################################################
##########                   WARNING EVENTS             ######################
##############################################################################
                                    eid4=7
                                    cmd="wevtutil qe Microsoft-Windows-Backup /f:text /q:*[System/EventID=%s]   /rd:true /c:1" %(eid4)
                                    obj = subprocess.Popen(cmd, shell = True, stdout = PIPE, stderr = PIPE)
                                    out, err = obj.communicate()
                                    if err:
                                        print err
                                    else:
                                        d5=re.findall('Date: (.*)T',out)
                                        if tdy == d5[0]:
                                            print "\t\t*)WARNING ERROR OCCURED..."
                                            des3=re.findall('Description:\s*(.*)', out)
                                            print "\t\t\t*)"+des3[0]
                                            alert(1)
                                        else:
##############################################################################
##########                   FAILED EVENTS             #######################
##############################################################################
                                            eid5=20
                                            cmd="wevtutil qe Microsoft-Windows-Backup /f:text /q:*[System/EventID=%s]   /rd:true /c:1" %(eid5)
                                            obj = subprocess.Popen(cmd, shell = True, stdout = PIPE, stderr = PIPE)
                                            out, err = obj.communicate()
                                            if err:
                                                print err
                                            else:
                                                d=out
                                                if d:
                                                    d6=re.findall('Date: (.*)T',d)
                                                    if tdy == d6[0]:
                                                        print "\t\t*)BACKUP FAILED ..."
                                                        if not os.path.isfile(os.path.join(workdir, "Failed.txt")):
                                                            with open(os.path.join(workdir, "Failed.txt"), 'w+') as fe:
                                                                fe.write(str(val))
                                                            print "\t\t\t*)Backup Failed count: "+str(val)
                                                        else:
                                                            with open(os.path.join(workdir, "Failed.txt"), 'r') as fe:
                                                                dm=fe.readlines()
                                                                for i, line in enumerate(dm):
                                                                    if i == 0:
                                                                        dt=val+int(line)
                                                                        with open(os.path.join(workdir, "Failed.txt"), 'w+') as fe:
                                                                            fe.write(str(dt))
                                                                print "\t\t\t*)Backup Failed count: "+str(dt)
                                                                if des4[0]:
                                                                    print "\t\t\t*)"+des4[0]
                                                                    alert(1)
                                                                else:
                                                                    print "\t\t\t*)Couldn't retrieve Description for FAILED EVENTS" 
                        else:
                            print "\t\t*)Backup still not completed."
                else:
                    print "\t\t*)Couldn't find events for Backup Started"
