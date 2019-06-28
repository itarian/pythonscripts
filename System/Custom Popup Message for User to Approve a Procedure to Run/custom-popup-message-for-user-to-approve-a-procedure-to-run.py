title=u"Hi press YES to continue ,NO to stop ." ## Define your message here 
message=u"Message from: ADMINISTRATOR" # 
import sys 
import ctypes
from threading import Timer
ki=ctypes.windll.user32.MessageBoxW(None,title, message, 3)
if ki==6:
    print "User said Yes"
elif ki == 7:
    print "User said NO"
    sys.exit(0)
else:
    print "User has cancelled the operation exiting from program"
    sys.exit(0)
#***************************************************************************************************************
#   Add your code below

print "Custom  code which is added is Running "
