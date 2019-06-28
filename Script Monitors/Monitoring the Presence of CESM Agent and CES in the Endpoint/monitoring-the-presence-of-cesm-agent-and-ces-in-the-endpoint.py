# The script is a template to CheckPresenceOfTheComodoProducts UAC status on device.
# Please use "alert(1)" to turn on the monitor(trigger an alert)
# Please use "alert(0)" to turn off the monitor(disable an alert)
# Please do not change above block and write your script below

"""Variable section"""
ESM = "COMODO ESM Agent"
CES = "COMODO Endpoint Security"
CCS = "COMODO Client - Security"
CAVS = "COMODO Antivirus for Servers"
# Version_of_the_CES = "If CES has the name COMODO Client - Security add the version here"
Version = "8.3.0.5204"
"""Variable section"""

""" Module import section """
import os
import ctypes
import sys
from subprocess import PIPE, Popen
import datetime
import re
""" Module import section """


Os_Path = r"C:\Program Files (x86)"
if os.path.exists(Os_Path):
    PathForErrorStatusFile = r"{0}\Program Files (x86)\COMODO\Comodo ITSM\rmmlogs\ErrorStatusFile.txt".format(os.environ['systemdrive'])
else:
    PathForErrorStatusFile = r"{0}\Program Files\COMODO\Comodo ITSM\rmmlogs\ErrorStatusFile.txt".format(os.environ['systemdrive'])

""" Class section """
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection

    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))

    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
""" Class section """

with disable_file_system_redirection():
    guid = os.popen(
        'wmic product get name,version| findstr /i /c:"COMODO Endpoint Security" /c:"COMODO ESM Agent" /c:"COMODO Antivirus for Servers" /c:"COMODO Client - Security"| sort').read()

print(guid)

# Checking type of the system and settings the right path for TimeStampFile
Path_for_time_stamp_file = r""
Os_Path = r"C:\Program Files (x86)"
if os.path.exists(Os_Path):
    Path_for_time_stamp_file = r"{0}\Program Files (x86)\COMODO\Comodo ITSM\rmmlogs\TimeStampStatus.txt".format(os.environ['systemdrive'])
else:
    Path_for_time_stamp_file = r"{0}\Program Files\COMODO\Comodo ITSM\rmmlogs\TimeStampStatus.txt".format(os.environ['systemdrive'])


# Send alert
def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))


# Run command in CMD
def DoCommandInCMD(command, output=False):
    with disable_file_system_redirection():
        objt = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = objt.communicate()
        ret = objt.returncode
    if not out:
        return ret
    else:
        return '%s\n%s' % (out, err)

# Check if timestamp file is present and comparing reboot time with the time in the file
def CheckTimeStampStatusFile():
    if os.path.isfile(Path_for_time_stamp_file):
        if os.path.isfile(r"{0}\pagefile.sys".format(os.environ['systemdrive'])):
            BootTimeFileTime = int("20" + datetime.datetime.fromtimestamp(os.path.getmtime(r"{0}\pagefile.sys".format(os.environ['systemdrive']))).strftime("%y%m%d%H%M%S"))
        else:
            BootTimeFileTime = int(re.sub("\D", "", str(DoCommandInCMD('wmic os get lastbootuptime | findstr "2018"', True)))[0:14])
        TimeStampFileTime = int(open(Path_for_time_stamp_file, "r").read())
        if BootTimeFileTime > TimeStampFileTime:
            os.remove(Path_for_time_stamp_file)
            return True
        else:
            print("Reboot is not performed yet")
            return False
    else:
        print("There is no timestamp file")
        return True



"""Logic section"""
if CheckTimeStampStatusFile():
    if guid:
        if (guid.find(ESM) != -1) or (guid.find(CES) != -1) or (guid.find(Version) != -1) or (guid.find(CAVS) != -1):
            print('ESM or CES or CCS ' + Version + ' or CAVS or their combination are present on the machine')
            alert(1)
        elif guid.find(CCS) != -1:
            print('ESM or CES or CCS ' + Version + ' is NOT present and latest CCS is present')
            alert(0)
    else:
        if os.path.isfile("{0}\Program Files\COMODO\COMODO Internet Security\cmdagent.exe".format(os.environ['systemdrive'])):
            print("cmdagent.exe is present")
            alert(0)
        else:
            print("No CCS OR CES OR CESM Installed in the system, cmdagent is not detected")
            alert(1)
else:
    alert(0)
"""Logic section"""
