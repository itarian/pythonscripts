import ctypes, ctypes.wintypes
class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
      ('cbSize', ctypes.wintypes.UINT),
      ('dwTime', ctypes.wintypes.DWORD),
      ]

PLASTINPUTINFO = ctypes.POINTER(LASTINPUTINFO)
user32 = ctypes.windll.user32
GetLastInputInfo = user32.GetLastInputInfo
GetLastInputInfo.restype = ctypes.wintypes.BOOL
GetLastInputInfo.argtypes = [PLASTINPUTINFO]
kernel32 = ctypes.windll.kernel32
GetTickCount = kernel32.GetTickCount
Sleep = kernel32.Sleep
def convertMillis(millis):
     seconds=(millis/1000)%60
     minutes=(millis/(1000*60))%60
     hours=(millis/(1000*60*60))%24
     return seconds, minutes, hours
def idle_time(idle_time=60):
    lasttime = None
    idle_time_ms = int(idle_time*1000)
    liinfo = LASTINPUTINFO()
    liinfo.cbSize = ctypes.sizeof(liinfo)
    while True:
        GetLastInputInfo(ctypes.byref(liinfo))
        elapsed = GetTickCount() - liinfo.dwTime
        GetLastInputInfo(ctypes.byref(liinfo))
        if lasttime is None: lasttime = liinfo.dwTime
        if lasttime != liinfo.dwTime:
            millis=elapsed
            con_sec, con_min, con_hour = convertMillis(int(millis))
            print "Computer IDLE time in Hours,Minutes and Seconds"
            print("{0}:{1}:{2}".format(con_hour, con_min, con_sec))
            break
def test():
    idle_time(10)
if __name__=='__main__':
    test()
