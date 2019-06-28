import os
import ctypes
from subprocess import PIPE, Popen

def oscmd(command):
    obj = os.popen(command).read()
    return obj.strip()

result=''
detected_drives=oscmd('wmic logicaldisk get name')
required_drive_letters=[i.strip() for i in detected_drives.split('\n') if i.strip()][1:]
print 'list of Disk Drives in the system on the following:'
print required_drive_letters
if required_drive_letters:
    for i in required_drive_letters:
        other_drive_fix=oscmd('chkdsk %s'%i)
        trimed_other_drive_fix=''
        if other_drive_fix:
            for a in other_drive_fix.split('\r'):
                if 'progress' not in a.lower() and 'percent' not in a.lower():
                        if a.strip():
                                trimed_other_drive_fix+=a
        result+='%s\n%s\n%s\n\n'%('Result of [%s] Drive: '%i, '.'*30, trimed_other_drive_fix)
print result
