# Please use "alert(1)" to turn on the monitor(trigger an alert)
# Please use "alert(0)" to turn off the monitor(disable an alert)


import os
import sys
import _winreg
import filecmp
import difflib

def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))

s=0
cmd=r"get-winevent -FilterHashtable @{Logname='Microsoft-Windows-Bitlocker/Bitlocker Management';ID=782}  -MaxEvents 1"
    
try:
        workdir=os.environ['PROGRAMDATA']+r'\temp'
        if not os.path.exists(workdir):
            os.mkdir(workdir)      
except:
        workdir=os.environ['SYTEMDRIVE']

old_file=workdir+r'\old_Bitlocker.txt'
new_file=workdir+r'\new_Bitlocker.txt'

def compare(event_logs):
    
    flag=0
    if False==0:
        
        with open(old_file) as file1:
           with open(new_file) as file2:
               diff = set(file1).difference(file2)
               if not diff:
                   s=0
                   return s

               else:
                   s=1
                   print event_logs
                   return s

                     
def create_old(cmd):
    cmd1=r"powershell.exe "+cmd
    
    event_logs=os.popen(cmd1).read()

    if not event_logs:
        print "Couldn't check for Event Logs with old file creation"
    else:
        with open(old_file, "wb") as f:
            f.write(event_logs)


def Bitlocker(cmd):
    import os
    import re
    import sys
    import xml.etree.ElementTree as ET
    import getpass
    import socket
    cmd1=r"powershell.exe "+cmd
    
    event_logs=os.popen(cmd1).read()

    if not event_logs:
        df=0
        print "Couldn't check for Event Logs"
        return df
    else:
        with open(new_file, "wb") as f:
            f.write(event_logs)
        v=compare(event_logs)
        return v

def remove():
    os.remove(old_file)
    os.rename(new_file,old_file)
    

if os.path.exists(workdir+r'\old_Bitlocker.txt'):
    df=Bitlocker(cmd)
else:
    create_old(cmd)
    df=Bitlocker(cmd)


if df>0:
    print "\nBitlocker has been recently Unlocked\n"
    alert(1)
else :
    print "\nNo Bitlocker has been recently Unlocked\n"
    alert(0)

remove()
