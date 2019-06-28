i= itsm.getParameter('parameterName')  # Provide the time in sec (60 sec = 1 min) 
import sys
import time


def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))


if sys.platform == 'win32':
    from ctypes import *
    
    class LASTINPUTINFO(Structure):
        _fields_ = [
            ('cbSize', c_uint),
            ('dwTime', c_int),
        ]
        
    def get_idle_duration():
        lastInputInfo = LASTINPUTINFO()
        lastInputInfo.cbSize = sizeof(lastInputInfo)
        if windll.user32.GetLastInputInfo(byref(lastInputInfo)):
            millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
            return millis / 1000.0
        else:
            return 0
else:
    def get_idle_duration():
        return 0

time.sleep(int(i))

    
if True:
    duration = get_idle_duration()
   

if int(i) < duration:
    print "System is in idle state"
   
else:
    print "System is in active state"
