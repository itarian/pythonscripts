import ctypes
import sys
import os
k=os.popen("wmic cpu get loadpercentage").read().split()[-1]
print "CPU UTILIZATION :\n"
print '\t\tCPU PERCENTAGE:',k+"%"

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]

    def __init__(self):
        # have to initialize this to the size of MEMORYSTATUSEX
        self.dwLength = ctypes.sizeof(self)
        super(MEMORYSTATUSEX, self).__init__()

stat = MEMORYSTATUSEX()
ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
print "\nMEMORY UTILIZATION :\n"
print("\t\tMemoryLoad PERCENTAGE: %d%%" % (stat.dwMemoryLoad))




drive=os.popen('wmic logicaldisk WHERE DriveType=3 get name').read()

list_of_drives=drive.split()[1:] 
percent=[]
def disk_usage(path):
    _, total, free = ctypes.c_ulonglong(), ctypes.c_ulonglong(), \
                       ctypes.c_ulonglong()
    if sys.version_info >= (3,) or isinstance(path, unicode):
        fun = ctypes.windll.kernel32.GetDiskFreeSpaceExW
    else:
        fun = ctypes.windll.kernel32.GetDiskFreeSpaceExA
    ret = fun(path, ctypes.byref(_), ctypes.byref(total), ctypes.byref(free))
    if ret == 0:
        raise ctypes.WinError()
    used = total.value - free.value
    up=round(float(free.value)/float(total.value)*100)
    percent.append(up)
    return [total.value, used, free.value]

def bytes2human(n):
    symbols = (' KB', ' MB', ' GB', ' TB', ' PB', ' EB', ' ZB', ' YB')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10 
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return n
k=[]
k1=0
for i in list_of_drives:
    for j in disk_usage(i):
        k.append(j)


fnl=[]
for i in k:
    fnl.append(bytes2human(i))
    
j=0
for i in list_of_drives:
    fnl.insert(j,i)    
    j=j+4

path=os.environ['Programdata']+'\storage.csv'
print "\nSTORAGE UTILIZATION :\n"
topic=['Drive Name','Total Size','Used Size','Free Size']
print("".join(str(i.ljust(25)) for i in topic ))
for i in range(1,len(fnl)):
    if i%4==0:
        fnl.insert(i,'\n'.rjust(25))

print("".join(str(i.ljust(25)) for i in fnl))
