########################################################################################################################
# Do you want to show Installation notes - Give showwarn "yes" or "no":
showwarn = "yes"
# Do you want to enable MSI Installation log?
msiLogs = "yes"
########################################################################################################################
Source_Path = r'\\COLOR\share'       # Provide the network share file path
File_Name_64 = r'CIS_x64.msi'  # Enter the .msi file name for 64 bit
File_Name_86 = r'CIS_x86.msi'  # Enter the .msi file name for 32 bit
########################################################################################################################

import os
from subprocess import PIPE, Popen
import shutil
import ctypes
import re
import time
import datetime

if msiLogs is "yes":
    print("MSI Logs are enabled")
    OsPath = r"C:\Program Files (x86)"
    if os.path.exists(OsPath):
        msiLogSwitch = r' /lv*x "C:\Program Files (x86)\COMODO\Comodo ITSM\rmmlogs\CES_Install_MSI ' + str(
            datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")) + '.log"'
    else:
        msiLogSwitch = r' /lv*x "C:\Program Files\COMODO\Comodo ITSM\rmmlogs\CES_Install_MSI ' + str(
            datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")) + '.log"'


class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection

    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))

    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


def check():
    with disable_file_system_redirection():
        inst = os.popen("wmic product get name,identifyingnumber").read()
    return inst


def ecmd(command, output=False):
    with disable_file_system_redirection():
        objt = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = objt.communicate()
        ret = objt.returncode
    if not out:
        return ret
    else:
        return '%s\n%s' % (out, err)


find = re.findall('{.*}\s\sCOMODO\sClient\s-\sSecurity', check())
if len(find) == 0:
    print("Comodo Client Security is not installed on the end point")
    EnvTemp = os.environ['ProgramData']
    Dest_Path = os.path.join(EnvTemp, r'Comodo')
    SP_64 = os.path.join(Source_Path, File_Name_64)
    SP_86 = os.path.join(Source_Path, File_Name_86)
    DP_64 = os.path.join(Dest_Path, File_Name_64)
    DP_86 = os.path.join(Dest_Path, File_Name_86)
    Install_exception = 0
    OsPath = r"C:\Program Files (x86)"
    if os.path.exists(OsPath):
        print "64"
        if not os.path.exists(Dest_Path):
            os.makedirs(Dest_Path)
            print("Folder for CCS is created")
        if os.path.isdir(Dest_Path):
            print('"' + Dest_Path + '"' + " folder exists")
        else:
            print('"' + Dest_Path + '"' + " folder do NOT exists")
            try:
                os.remove(DP_64)
            except OSError:
                pass
        print("Needed files will be copied from a shared folder %s" % Source_Path)
        shutil.copy(SP_64, DP_64)
        time.sleep(300)
        if os.path.getsize(SP_64) == os.path.getsize(DP_64):
            print("Files were successfully copied")
        else:
            print("Unable to copy file. %s" % File_Name_64)
            exit(code = 1)
        time.sleep(300)
        command1 = 'msiexec /i  "' + DP_64 + '"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=1 CES_FIREWALL=1 CES_ANTIVIRUS=1 INSTALLFIREWALL=1' + msiLogSwitch
        if ecmd(command1, True) == 3010:
            CMD_1='"C:\Program Files (x86)\COMODO\Comodo ITSM\ITSMService.exe" -c 4'
            com=os.popen(CMD_1).read()
            pass
        else:
            raise Exception("Failed to install CCS. Please check MSI logs for details:%s" % str(msiLogSwitch)[7:])
        if showwarn is "yes":
            print(ecmd(r'msg * /time:30 CCS installation is started. Do not restart PC until next announcement.', True))
        print("ITSM is trying to connect to the CCS")
        time.sleep(300)
        print("ITSM is connected to the CCS")
        os.remove(DP_64)
        print("Installation files have been removed")
        print('Comodo Client Security installed Successfully')
        print('System will restart in 5 minutes')
        print(ecmd(r'msg * /time:30 CCS installation is finished.You may restart PC to complete installation.', True))

    else:
        if not os.path.exists(Dest_Path):
            os.makedirs(Dest_Path)
            print("Folder for CCS is created")
        if os.path.isdir(Dest_Path):
            print('"' + Dest_Path + '"' + " folder exists")
        else:
            print('"' + Dest_Path + '"' + " folder do NOT exists")
            try:
                os.remove(DP_86)
            except OSError:
                pass
        print("Needed files will be copied from a shared folder %s" % Source_Path)
        shutil.copy(SP_86, DP_86)
        if os.path.getsize(SP_86) == os.path.getsize(DP_86):
            print("Files were successfully copied")
        else:
            print("Unable to copy file. %s" % File_Name_86)
            exit(code = 1)
        time.sleep(300)
        command1 = 'msiexec /i  "' + DP_86 + '"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=1 CES_FIREWALL=1 CES_ANTIVIRUS=1 INSTALLFIREWALL=1' + msiLogSwitch
        if ecmd(command1, True) == 3010:
            CMD_1='"C:\Program Files\COMODO\Comodo ITSM\ITSMService.exe" -c 4'
            com=os.popen(CMD_1).read()
            pass
        else:
            raise Exception("Failed to install CCS. Please check MSI logs for details:%s" % str(msiLogSwitch)[7:])
        if showwarn is "yes":
            print(ecmd(r'msg * /time:30 CCS installation is started. Do not restart PC until next announcement.', True))
        print("ITSM is trying to connect to the CCS")
        time.sleep(300)
        print("ITSM is connected to the CCS")
        os.remove(DP_86)
        print("Installation files have been removed")
        print('Comodo Client Security installed Successfully')
        print(ecmd(r'msg * /time:30 CCS installation is finished.You may restart PC to complete installation.', True))
else:
    print("Comodo Client Security is installed on the End point")
