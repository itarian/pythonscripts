import os
import platform
import sys
import ctypes

from sys import platform as _platform
if _platform == "win32":
    windows_32=platform.version()
    sys=platform.system()
    print"OS version : "+sys +' ' +windows_32
elif _platform == "win64":
    sys_64=platform.system()
    windows_64=platform.version()
    print"The OS version : "+sys_64 +' ' +windows_64
elif _platform == "linux" or _platform == "linux2":
    lin=platform.system()
    linux=platform.version()
    print"The OS version : " +lin +' '+linux
elif _platform == "darwin":
    Mac=platform.system()
    Mac_os=platform.version()
    print"The OS version : " +Mac +' ' +Mac_os
    
   

    
