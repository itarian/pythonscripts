This is the Custom Monitoring Script which is used to Suspend the Bit-locker protection if any Reboots Required in the System and also Resume the Bit-locker protection after gets the Reboot Successfully. it will intimate User to reboot their System if any Reboots Required at the time will suspend the Bit-locker protection


Checking the following Services which are the things needs the reboot if any application or updates to be installed newly on the system. 
Eg:

RebootPending      : True

If anyone of the Service is True then the system Requires the Reboot.
Eg:  RebootPending      : True


Note:
Don't Run this Script as Normal Procedure 

Please Refer the Following wiki Guide For Running The Custom Monitoring Procedure:
https://wiki.comodo.com/frontend/web/topic/how-to-use-custom-script-procedure-monitoring