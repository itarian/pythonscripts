#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('variableName') with that parameter's name
#########################Configuration#Section##########################################################################
# Do you want to download the package from COMODO servers?
comodoservers = "yes"
# if comodo = "yes" the package will be downloaded from:
# https://download.comodo.com/itsm/CIS_x64.msi
# https://download.comodo.com/itsm/CIS_x86.msi
# if comodo = "no" please provide the shared folder path and the .msi names:
SharedFolderPath = r'path'
CISx64Name = r'fileName'
CISx86Name = r'fileName'
# Please choose what to be installed before the profile is applied.
# You can use "yes" or "no"
#Desktop
Containment = "yes"
Antivirus = "yes"
Firewall = "no"
#Server
ContainmentS = "yes"
AntivirusS = "yes"
# If Antivirus = "yes" do you want to download the initial Database from a shared folder ?
# ( Database is automatically updated from Comodo servers after 1 hour as default or after a reboot )
Database = "no"
# If Database = "yes" you can download the latest database from this link and place it on shared folder:
# https://www.comodo.com/home/internet-security/updates/vdp/database.php
SharedFolderPathCAV = r'path'
# FileNameCAV = r'xxxx.cav'
FileNameCAV = r'fileName'
# After CCS is installed do you want to supress the reboot on the endpoint?
SuppressReboot = "yes"
# If reboot = "no" by default you have 5 minutes with a comment "Your device will reboot in 5 minutes because it's required by your administrator"
reboottime = "300"
# Do you want to show installation notes?
notes = "yes"
# Do you want to enable MSI Installation log?
scan="yes"
#scan option is working in all windows except windows 7 and also it perform only if suppressReboot="No"
msiLogs = "yes"
########################################################################################################################


import os
from subprocess import PIPE, Popen
import shutil
import ctypes
import re
import datetime
import platform

try:
    import winreg as _winreg
except ImportError:
    try:
        import _winreg
    except ImportError:
        pass
import ssl
import time

try:
    import urllib.request as urllib2
except ImportError:
    try:
        import urllib2
    except ImportError:
        pass

def GetWindowsEdition(Key_name):
	val = ""
	try:
		reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
		ok = _winreg.OpenKey(reg, Key_name, 0, _winreg.KEY_WOW64_32KEY | _winreg.KEY_READ)
		val = _winreg.QueryValueEx(ok, "ProductName")[0]
		_winreg.CloseKey(ok)
		return val
	except Exception as exception:
		val = "Windows Registry Exception: " + str(exception)
		return val

WindowsVersion = GetWindowsEdition('SOFTWARE\Microsoft\Windows NT\CurrentVersion')

def Triggerfullscan():
    import os
    ps_content=r'''
Get-CimInstance -Namespace root/cis AvProfile -Filter "Name = 'Full Scan'" | Invoke-CimMethod -MethodName StartScan
'''
    file_name='powershell_file.ps1'
    file_path=os.path.join(os.environ['TEMP'], file_name)
    with open(file_path, 'wb') as wr:
        wr.write(ps_content)
    ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
    print (ecmd('powershell "%s"'%file_path))

os_details = platform.release()
  
msiLogSwitch = ""

if msiLogs is "yes":
    OsPath = r"C:\Program Files (x86)"
    if os.path.exists(OsPath):
        msiLogSwitch = r' /lv*x "C:\Program Files (x86)\COMODO\Comodo ITSM\rmmlogs\CES_Install_MSI ' + str(
            datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")) + '.log"'
    else:
        msiLogSwitch = r' /lv*x "C:\Program Files\COMODO\Comodo ITSM\rmmlogs\CES_Install_MSI ' + str(
            datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")) + '.log"'

t1 = int(reboottime) / 60
rebootcomment = "Your device will reboot in " + str(t1) + " minutes because it's required by your administrator"


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


def Download1(Download_URL, Download_Path):
    print('Downloading required Comodo Client Security installation files')
    fileName = Download_URL.split('/')[-1]
    DownTo = os.path.join(Download_Path, fileName)
    try:
        context = ssl._create_unverified_context()
        f = urllib2.urlopen(Download_URL, context=context)
    except:
        f = urllib2.urlopen(Download_URL)
    data = f.read()
    with open(DownTo, "wb") as code:
        code.write(data)
    time.sleep(300)
    print('Comodo Client security has been successfully downloaded here ' + DownTo)
    return DownTo


find = re.findall('{.*}\s\sCOMODO\sClient\s-\sSecurity', check())
# Check if CCS is installed on the end point
if len(find) == 0:
    print("Comodo Client Security is not installed on the End point")
    # Checks type of the system
    OsPath = r"C:\Program Files (x86)"
    # If system is 64 bit
    if os.path.exists(OsPath):
        print("System type 64 bit")
        # Download and install CCS from the link
        if comodoservers is "yes":
            print("Installation files will be downloaded from Comodo Servers")
            Download_URL = "https://download.comodo.com/itsm/CIS_x64.msi"
            Download_Path = os.environ['PROGRAMDATA']
            path = Download1(Download_URL, Download_Path)
            if not ("Server" in WindowsVersion or "server" in WindowsVersion):
                c = "0"
                a = "0"
                f = "0"
                if Containment is "yes":
                    print("Containment component will be installed")
                    c = "1"
                else:
                    print("Containment component will not be installed")
                    c = "0"
                if Antivirus is "yes":
                    print("Antivirus component will be installed")
                    a = "1"
                else:
                    print("Antivirus component will not be installed")
                    a = "0"
                if Firewall is "yes":
                    print("Firewall component will be installed")
                    f = "1"
                else:
                    print("Firewall component will not be installed")
                    f = "0"
                if notes is "yes":
                    print(ecmd(
                        r'msg * /time:30 Comodo Client - Security installation has started. Do not restart PC until next announcement.',
                        True))
                command1 = 'msiexec /i  "' + path + '"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=' + c + ' CES_FIREWALL=' + f + ' CES_ANTIVIRUS=' + a + ' INSTALLFIREWALL=' + f + msiLogSwitch
                if ecmd(command1, True) == 3010:
                    ecmd('"C:\Program Files (x86)\COMODO\Comodo ITSM\ITSMService.exe" -c 4',True)
                    pass
                else:
                    raise Exception("Failed to install CCS. Please check MSI logs for details:%s" % str(msiLogSwitch)[7:])
            else:
                c = "0"
                a = "0"
                if ContainmentS is "yes":
                    print("Containment component will be installed")
                    c = "1"
                else:
                    print("Containment component will not be installed")
                    c = "0"
                if AntivirusS is "yes":
                    print("Antivirus component will be installed")
                    a = "1"
                else:
                    print("Antivirus component will not be installed")
                    a = "0"
                if notes is "yes":
                    print(ecmd(
                        r'msg * /time:30 Comodo Client - Security installation has started. Do not restart PC until next announcement.',
                        True))
                command1 = 'msiexec /i  "' + path + '"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=' + c + ' CES_FIREWALL=0 CES_ANTIVIRUS=0 AV_FOR_SERVERS=' + a + msiLogSwitch
                if ecmd(command1, True) == 3010:
                    ecmd('"C:\Program Files (x86)\COMODO\Comodo ITSM\ITSMService.exe" -c 4',True)
                    pass
                else:
                    raise Exception("Failed to install CCS. Please check MSI logs for details:%s" % str(msiLogSwitch)[7:])
            print("Please wait until CCS will be installed")
            time.sleep(300)
            os.remove(path)
            print('Comodo Client Security was successfully installed')
            print("Installation files have been successfully removed")
            if Antivirus is "yes":
                print("Antivirus component was installed")
                if Database is "no":
                    print("Database will be updated accordingly to the schedule")
                    if SuppressReboot is "yes":
                        print("Reboot of the system was suppressed")
                        if notes is "yes":
                            print(ecmd(r'msg * /time:30 CCS installation is finished. You may restart PC to complete installation.',True))
                    else:
                        print ("Successfully started the Full scan in CCS...")
                        if "7" in os_details:
                            pass
                        else:
                          if scan is "yes":
                                Triggerfullscan()
                                print("Reboot of the system wasn't suppressed")
                                print('System will restart in ' + str(t1) + ' minutes')
                                print(ecmd(r'shutdown.exe -r -t ' + reboottime + ' /f /c "' + rebootcomment + '"', True))
                else:
                    print("Database will be imported from the shared folder")
                    if len(re.findall('{.*}\s\sCOMODO\sClient\s-\sSecurity', check())) != 0:
                        print("COMODO Client Security is installed on the PC")
                        print("Antivirus signature database out of date")
                        Source_Path = SharedFolderPathCAV
                        EnvTemp = os.environ['PROGRAMDATA']
                        Dest_Path = os.path.join(EnvTemp, r'Comodo')
                        File_Name_CAV = FileNameCAV
                        SP_CAV = os.path.join(Source_Path, File_Name_CAV)
                        DP_CAV = os.path.join(Dest_Path, File_Name_CAV)
                        if os.path.exists(SP_CAV):
                            print("Database source path exists")
                        if not os.path.exists(Dest_Path):
                            os.makedirs(Dest_Path)
                            print("Destination path was created")
                        if os.path.isdir(Dest_Path):
                            print('"' + Dest_Path + '"' + " folder exists")
                        else:
                            print('"' + Dest_Path + '"' + " folder do NOT exists")
                        try:
                            os.remove(DP_CAV)
                        except OSError:
                            pass
                        shutil.copy(SP_CAV, DP_CAV)
                        if os.path.getsize(SP_CAV) == os.path.getsize(DP_CAV):
                            print("Database files were copied successfully")
                        else:
                            print("Database files weren't copied")
                        time.sleep(300)
                        command1 = '"C:\Program Files\COMODO\COMODO Internet Security\cfpconfg.exe" --importAVDB "' + DP_CAV + '"'
                        print(ecmd(command1, True))
                        print('Antivirus signature database was updated Successfully')
                        print("ITSM agent is trying to connect to the CCS")
                        time.sleep(300)
                        if SuppressReboot is "yes":
                            print("Reboot of the system was suppressed")
                            if notes is "yes":
                                print(ecmd(
                                    r'msg * /time:30 CCS installation is finished. You may restart PC to complete installation.',
                                    True))
                        else:
                            print ("Successfully started the Full scan in CCS...")
                            if "7" in os_details:
                                pass
                            else:
                                if scan is "yes":
                                    Triggerfullscan()
                                    print("Reboot of the system wasn't suppressed")
                                    print('System will restart in ' + str(t1) + ' minutes')
                                    print(ecmd(r'shutdown.exe -r -t ' + reboottime + ' /f /c "' + rebootcomment + '"', True))
                    else:
                        print("COMODO Client Security is NOT present")
                        print("Endpoint will NOT reboot, regardless of the SuppressReboot settings")
            else:
                if SuppressReboot is "yes":
                    print("Reboot of the system was suppressed")
                    if notes is "yes":
                        print(ecmd(r'msg * /time:30 Comodo Client Security installation is finished. You may restart PC to complete installation.',True))
                else:
                    print("Reboot of the system was NOT suppressed")
                    print('System will restart in ' + str(t1) + ' minutes')
                    print(ecmd(r'shutdown.exe -r -t ' + reboottime + ' /f /c "' + rebootcomment + '"', True))
        # CCS will be installed from the shared folder
        else:
            print("Installation files will be copied from shared folder")
            Source_Path = SharedFolderPath
            EnvTemp = os.environ['ProgramData']
            Dest_Path = os.path.join(EnvTemp, r'Comodo')
            SP_64 = os.path.join(Source_Path, CISx64Name)
            DP_64 = os.path.join(Dest_Path, CISx64Name)
            if not os.path.exists(Dest_Path):
                os.makedirs(Dest_Path)
                print("Destination path was created")
            if os.path.isdir(Dest_Path):
                print('"' + Dest_Path + '"' + " folder exists")
            else:
                print('"' + Dest_Path + '"' + " folder do NOT exists")
            try:
                os.remove(DP_64)
            except OSError:
                pass
            shutil.copy(SP_64, DP_64)
            if os.path.getsize(SP_64) == os.path.getsize(DP_64):
                print("Installation files were copied successfully")
            else:
                print("Installation files weren't copied")
                exit(code=1)
            time.sleep(300)
            if os.path.getsize(SP_64) == os.path.getsize(DP_64):
                print("Database files were copied successfully")
            else:
                print("Database files weren't copied")
            time.sleep(300)
            if not ("Server" in WindowsVersion or "server" in WindowsVersion):
                c = "0"
                a = "0"
                f = "0"
                if Containment is "yes":
                    print("Containment component will be installed")
                    c = "1"
                else:
                    print("Containment component will not be installed")
                    c = "0"
                if Antivirus is "yes":
                    print("Antivirus component will be installed")
                    a = "1"
                else:
                    print("Antivirus component will not be installed")
                    a = "0"
                if Firewall is "yes":
                    print("Firewall component will be installed")
                    f = "1"
                else:
                    print("Firewall component will not be installed")
                    f = "0"
                if notes is "yes":
                    print(ecmd(r'msg * /time:30 CCS installation is started. Do not restart PC until next anouncement.',True))
                command1 = 'msiexec /i  "' + DP_64 + '"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=' + c + ' CES_FIREWALL=' + f + ' CES_ANTIVIRUS=' + a + ' INSTALLFIREWALL=' + f + msiLogSwitch
                if ecmd(command1, True) == 3010:
                    ecmd('"C:\Program Files (x86)\COMODO\Comodo ITSM\ITSMService.exe" -c 4',True)
                    pass
                else:
                    raise Exception("Failed to install CCS. Please check MSI logs for details:%s" % str(msiLogSwitch)[7:])
            else:
                c = "0"
                a = "0"
                if ContainmentS is "yes":
                    print("Containment component will be installed")
                    c = "1"
                else:
                    print("Containment component will not be installed")
                    c = "0"
                if AntivirusS is "yes":
                    print("Antivirus component will be installed")
                    a = "1"
                else:
                    print("Antivirus component will not be installed")
                    a = "0"
                if notes is "yes":
                    print(ecmd(r'msg * /time:30 CCS installation is started. Do not restart PC until next anouncement.',True))
                command1 = 'msiexec /i  "' + DP_64 + '"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=' + c + ' CES_FIREWALL=0 CES_ANTIVIRUS=0 AV_FOR_SERVERS=' + a + msiLogSwitch
                if ecmd(command1, True) == 3010:
                    ecmd('"C:\Program Files (x86)\COMODO\Comodo ITSM\ITSMService.exe" -c 4',True)
                    pass
                else:
                    raise Exception("Failed to install CCS. Please check MSI logs for details:%s" % str(msiLogSwitch)[7:])
            print("Please wait until CCS will be installed")
            time.sleep(300)
            os.remove(DP_64)
            print('Comodo Client Security was successfully installed')
            print("Installation files have been successfully removed")
            if Antivirus is "yes":
                print("Antivirus component was installed")
                if Database is "no":
                    print("Database will be updated accordingly to the schedule")
                    if SuppressReboot is "yes":
                        print("Reboot of the system was suppressed")
                        if notes is "yes":
                            print(ecmd(r'msg * /time:30 CCS installation is finished. You may restart PC to complete installation.',True))
                    else:
                        print ("Successfully started the Full scan in CCS...")
                        if "7" in os_details:
                            pass
                        else:
                            if scan is "yes":
                                Triggerfullscan()
                                print("Reboot of the system wasn't suppressed")
                                print('System will restart in ' + str(t1) + ' minutes')
                                print(ecmd(r'shutdown.exe -r -t ' + reboottime + ' /f /c "' + rebootcomment + '"', True))
                else:
                    print("Database will be imported from the shared folder")

                    if len(re.findall('{.*}\s\sCOMODO\sClient\s-\sSecurity', check())) != 0:
                        print("COMODO Client Security is installed on the PC")
                        print("Antivirus signature database out of date")
                        Source_Path = SharedFolderPathCAV
                        EnvTemp = os.environ['PROGRAMDATA']
                        Dest_Path = os.path.join(EnvTemp, r'Comodo')
                        File_Name_CAV = FileNameCAV
                        SP_CAV = os.path.join(Source_Path, File_Name_CAV)
                        DP_CAV = os.path.join(Dest_Path, File_Name_CAV)
                        if os.path.exists(SP_CAV):
                            print("Database path exists")
                        if not os.path.exists(Dest_Path):
                            os.makedirs(Dest_Path)
                            print("Destination folder was created")
                        if os.path.isdir(Dest_Path):
                            print('"' + Dest_Path + '"' + " folder exists")
                        else:
                            print('"' + Dest_Path + '"' + " folder do NOT exists")
                        try:
                            os.remove(DP_CAV)
                        except OSError:
                            pass
                        if os.path.getsize(SP_CAV) == os.path.getsize(DP_CAV):
                            print("Database files were copied successfully")
                        else:
                            print("Database files weren't copied")
                            exit(code = 1)
                        command1 = '"C:\Program Files\COMODO\COMODO Internet Security\cfpconfg.exe" --importAVDB "' + DP_CAV + '"'
                        print(ecmd(command1, True))
                        print('Antivirus signature database was updated Successfully')
                        print("ITSM agent is trying to connect to the CCS")
                        time.sleep(300)
                        if SuppressReboot is "yes":
                            print("Reboot of the system was suppressed")
                            if notes is "yes":
                                print(ecmd(
                                    r'msg * /time:30 CCS installation is finished. You may restart PC to complete installation.',
                                    True))
                        else:
                            print ("Successfully started the Full scan in CCS...")
                            if "7" in os_details:
                                pass
                            else:
                                if scan is "yes":
                                    Triggerfullscan()
                                    print("Reboot of the system wasn't suppressed")
                                    print('System will restart in ' + str(t1) + ' minutes')
                                    print(ecmd(r'shutdown.exe -r -t ' + reboottime + ' /f /c "' + rebootcomment + '"', True))
                    else:
                        print("COMODO Client Security is NOT present")
                        print("Endpoint will NOT reboot, regardless of the SuppressReboot settings")
            else:
                if SuppressReboot is "yes":
                    print("Reboot of the system was suppressed")
                    if notes is "yes":
                        print(ecmd(r'msg * /time:30 Comodo Client Security installation is finished. You may restart PC to complete installation.',True))
                else:
                    print("Reboot of the system was NOT suppressed")
                    print('System will restart in ' + str(t1) + ' minutes')
                    print(ecmd(r'shutdown.exe -r -t ' + reboottime + ' /f /c "' + rebootcomment + '"', True))
    else:
        # If system is 32 bit      
        print("System type 32 bit")
        # Download and install CCS from the link
        if comodoservers is "yes":
            print("Installation files will be downloaded from Comodo Servers")
            Download_URL = "https://download.comodo.com/itsm/CIS_x86.msi"
            Download_Path = os.environ['PROGRAMDATA']
            path = Download1(Download_URL, Download_Path)
            if not ("Server" in WindowsVersion or "server" in WindowsVersion):
                c = "0"
                a = "0"
                f = "0"
                if Containment is "yes":
                    print("Containment component will be installed")
                    c = "1"
                else:
                    print("Containment component will not be installed")
                    c = "0"
                if Antivirus is "yes":
                    print("Antivirus component will be installed")
                    a = "1"
                else:
                    print("Antivirus component will not be installed")
                    a = "0"
                if Firewall is "yes":
                    print("Firewall component will be installed")
                    f = "1"
                else:
                    print("Firewall component will not be installed")
                    f = "0"
                if notes is "yes":
                    print(ecmd(r'msg * /time:30 Comodo Client - Security installation has started. Do not restart PC until next announcement.',True))
                command1 = 'msiexec /i  "' + path + '"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=' + c + ' CES_FIREWALL=' + f + ' CES_ANTIVIRUS=' + a + ' INSTALLFIREWALL=' + f + msiLogSwitch
                if ecmd(command1, True) == 3010:
                    ecmd('"C:\Program Files\COMODO\Comodo ITSM\ITSMService.exe" -c 4',True)
                    pass
                else:
                    raise Exception(
                        "Failed to install CCS. Please check MSI logs for details:%s" % str(msiLogSwitch)[7:])
            else:
                c = "0"
                a = "0"
                if ContainmentS is "yes":
                    print("Containment component will be installed")
                    c = "1"
                else:
                    print("Containment component will not be installed")
                    c = "0"
                if Antivirus is "yes":
                    print("Antivirus component will be installed")
                    a = "1"
                else:
                    print("Antivirus component will not be installed")
                    a = "0"
                if notes is "yes":
                    print(ecmd(r'msg * /time:30 Comodo Client - Security installation has started. Do not restart PC until next announcement.',True))
                command1 = 'msiexec /i  "' + path + '"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=' + c + ' CES_FIREWALL=0 CES_ANTIVIRUS=0 AV_FOR_SERVERS=' + a + msiLogSwitch
                if ecmd(command1, True) == 3010:
                    ecmd('"C:\Program Files\COMODO\Comodo ITSM\ITSMService.exe" -c 4',True)
                    pass
                else:
                    raise Exception(
                        "Failed to install CCS. Please check MSI logs for details:%s" % str(msiLogSwitch)[7:])
            print("Please wait until CCS will be installed")
            time.sleep(300)
            os.remove(path)
            print('Comodo Client Security was successfully installed')
            print("Installation files have been successfully removed")
            if Antivirus is "yes":
                print("Antivirus component was installed")
                if Database is "no":
                    print("Database will be updated accordingly to the schedule")
                    if SuppressReboot is "yes":
                        print("Reboot of the system was suppressed")
                        if notes is "yes":
                            print(ecmd(r'msg * /time:30 CCS installation is finished. You may restart PC to complete installation.',True))
                    else:
                        print ("Successfully started the Full scan in CCS...")
                        if "7" in os_details:
                            pass
                        else:
                            if scan is "yes":
                                Triggerfullscan()
                                print("Reboot of the system wasn't suppressed")
                                print('System will restart in ' + str(t1) + ' minutes')
                                print(ecmd(r'shutdown.exe -r -t ' + reboottime + ' /f /c "' + rebootcomment + '"', True))
                else:
                    print("Database will be imported from the shared folder")
                    if len(re.findall('{.*}\s\sCOMODO\sClient\s-\sSecurity', check())) != 0:
                        print("COMODO Client Security is installed on the PC")
                        print("Antivirus signature database out of date")
                        Source_Path = SharedFolderPathCAV
                        EnvTemp = os.environ['PROGRAMDATA']
                        Dest_Path = os.path.join(EnvTemp, r'Comodo')
                        File_Name_CAV = FileNameCAV
                        SP_CAV = os.path.join(Source_Path, File_Name_CAV)
                        DP_CAV = os.path.join(Dest_Path, File_Name_CAV)
                        if os.path.exists(SP_CAV):
                            print("Database source path exists")
                        if not os.path.exists(Dest_Path):
                            os.makedirs(Dest_Path)
                            print("Destination path was created")
                        if os.path.isdir(Dest_Path):
                            print('"' + Dest_Path + '"' + " folder exists")
                        else:
                            print('"' + Dest_Path + '"' + " folder do NOT exists")
                        try:
                            os.remove(DP_CAV)
                        except OSError:
                            pass
                        shutil.copy(SP_CAV, DP_CAV)
                        if os.path.getsize(SP_CAV) == os.path.getsize(DP_CAV):
                            print("Database files were copied successfully")
                        else:
                            print("Database files weren't copied")
                        time.sleep(300)
                        command1 = '"C:\Program Files\COMODO\COMODO Internet Security\cfpconfg.exe" --importAVDB "' + DP_CAV + '"'
                        print(ecmd(command1, True))
                        print('Antivirus signature database was updated Successfully')
                        print("ITSM agent is trying to connect to the CCS")
                        time.sleep(300)
                        if SuppressReboot is "yes":
                            print("Reboot of the system was suppressed")
                            if notes is "yes":
                                print(ecmd(
                                    r'msg * /time:30 CCS installation is finished. You may restart PC to complete installation.',
                                    True))
                        else:
                            print ("Successfully started the Full scan in CCS...")
                            if "7" in os_details:
                                pass
                            else:
                                if scan is "yes":
                                    Triggerfullscan()
                                    print("Reboot of the system wasn't suppressed")
                                    print('System will restart in ' + str(t1) + ' minutes')
                                    print(ecmd(r'shutdown.exe -r -t ' + reboottime + ' /f /c "' + rebootcomment + '"', True))
                    else:
                        print("COMODO Client Security is NOT present")
                        print("Endpoint will NOT reboot, regardless of the SuppressReboot settings")
            else:
                if SuppressReboot is "yes":
                    print("Reboot of the system was suppressed")
                    if notes is "yes":
                        print(ecmd(
                            r'msg * /time:30 Comodo Client Security installation is finished. You may restart PC to complete installation.',
                            True))
                else:
                    print("Reboot of the system was NOT suppressed")
                    print('System will restart in ' + str(t1) + ' minutes')
                    print(ecmd(r'shutdown.exe -r -t ' + reboottime + ' /f /c "' + rebootcomment + '"', True))
        # CCS will be installed from the shared folder
        else:
            print("Installation files will be copied from shared folder")
            Source_Path = SharedFolderPath
            EnvTemp = os.environ['ProgramData']
            Dest_Path = os.path.join(EnvTemp, r'Comodo')
            SP_86 = os.path.join(Source_Path, CISx86Name)
            DP_86 = os.path.join(Dest_Path, CISx86Name)
            if not os.path.exists(Dest_Path):
                os.makedirs(Dest_Path)
                print("Destination path was created")
            if os.path.isdir(Dest_Path):
                print('"' + Dest_Path + '"' + " folder exists")
            else:
                print('"' + Dest_Path + '"' + " folder do NOT exists")
            try:
                os.remove(DP_86)
            except OSError:
                pass
            shutil.copy(SP_86, DP_86)
            if os.path.getsize(SP_86) == os.path.getsize(DP_86):
                print("Installation files were copied successfully")
            else:
                print("Installation files weren't copied")
                exit(code=1)
            time.sleep(300)
            if not ("Server" in WindowsVersion or "server" in WindowsVersion):
                c = "0"
                a = "0"
                f = "0"
                if Containment is "yes":
                    print("Containment component will be installed")
                    c = "1"
                else:
                    print("Containment component will not be installed")
                    c = "0"
                if Antivirus is "yes":
                    print("Antivirus component will be installed")
                    a = "1"
                else:
                    print("Antivirus component will not be installed")
                    a = "0"
                if Firewall is "yes":
                    print("Firewall component will be installed")
                    f = "1"
                else:
                    print("Firewall component will not be installed")
                    f = "0"
                if notes is "yes":
                    print(ecmd(r'msg * /time:30 CCS installation is started. Do not restart PC until next anouncement.',
                               True))
                command1 = 'msiexec /i  "' + DP_86 + '"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=' + c + ' CES_FIREWALL=' + f + ' CES_ANTIVIRUS=' + a + ' INSTALLFIREWALL=' + f + msiLogSwitch
                if ecmd(command1, True) == 3010:
                    ecmd('"C:\Program Files\COMODO\Comodo ITSM\ITSMService.exe" -c 4',True)
                    pass
                else:
                    raise Exception(
                        "Failed to install CCS. Please check MSI logs for details:%s" % str(msiLogSwitch)[7:])
            else:
                c = "0"
                a = "0"
                if Containment is "yes":
                    print("Containment component will be installed")
                    c = "1"
                else:
                    print("Containment component will not be installed")
                    c = "0"
                if Antivirus is "yes":
                    print("Antivirus component will be installed")
                    a = "1"
                else:
                    print("Antivirus component will not be installed")
                    a = "0"
                if notes is "yes":
                    print(ecmd(r'msg * /time:30 CCS installation is started. Do not restart PC until next anouncement.',
                               True))
                command1 = 'msiexec /i  "' + DP_86 + '"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=' + c + ' CES_FIREWALL=0 CES_ANTIVIRUS=0 AV_FOR_SERVERS=' + a + msiLogSwitch
                if ecmd(command1, True) == 3010:
                    ecmd('"C:\Program Files\COMODO\Comodo ITSM\ITSMService.exe" -c 4',True)
                    pass
                else:
                    raise Exception(
                        "Failed to install CCS. Please check MSI logs for details:%s" % str(msiLogSwitch)[7:])
            print("Please wait until CCS will be installed")
            time.sleep(300)
            os.remove(DP_86)
            print('Comodo Client Security was successfully installed')
            print("Installation files have been successfully removed")
            if Antivirus is "yes":
                print("Antivirus component was installed")
                if Database is "no":
                    print("Database will be updated accordingly to the schedule")
                    if SuppressReboot is "yes":
                        print("Reboot of the system was suppressed")
                        if notes is "yes":
                            print(ecmd(
                                r'msg * /time:30 CCS installation is finished. You may restart PC to complete installation.',
                                True))
                    else:
                        print ("Successfully started the Full scan in CCS...")
                        if "7" in os_details:
                                pass
                        else:
                            if scan is "yes":
                                Triggerfullscan()
                                print("Reboot of the system wasn't suppressed")
                                print('System will restart in ' + str(t1) + ' minutes')                      
                                print(ecmd(r'shutdown.exe -r -t ' + reboottime + ' /f /c "' + rebootcomment + '"', True))
                else:
                    print("Database will be imported from the shared folder")

                    if len(re.findall('{.*}\s\sCOMODO\sClient\s-\sSecurity', check())) != 0:
                        print("COMODO Client Security is installed on the PC")
                        print("Antivirus signature database out of date")
                        Source_Path = SharedFolderPathCAV
                        EnvTemp = os.environ['PROGRAMDATA']
                        Dest_Path = os.path.join(EnvTemp, r'Comodo')
                        File_Name_CAV = FileNameCAV
                        SP_CAV = os.path.join(Source_Path, File_Name_CAV)
                        DP_CAV = os.path.join(Dest_Path, File_Name_CAV)
                        if os.path.exists(SP_CAV):
                            print("Database path exists")
                        if not os.path.exists(Dest_Path):
                            os.makedirs(Dest_Path)
                            print("Destination folder was created")
                        if os.path.isdir(Dest_Path):
                            print('"' + Dest_Path + '"' + " folder exists")
                        else:
                            print('"' + Dest_Path + '"' + " folder do NOT exists")
                        try:
                            os.remove(DP_CAV)
                        except OSError:
                            pass
                        shutil.copy(SP_CAV, DP_CAV)
                        if os.path.getsize(SP_CAV) == os.path.getsize(DP_CAV):
                            print("Database files were copied successfully")
                        else:
                            print("Database files weren't copied")
                        command1 = '"C:\Program Files\COMODO\COMODO Internet Security\cfpconfg.exe" --importAVDB "' + DP_CAV + '"'
                        print(ecmd(command1, True))
                        print('Antivirus signature database was updated Successfully')
                        print("ITSM agent is trying to connect to the CCS")
                        time.sleep(300)
                        if SuppressReboot is "yes":
                            print("Reboot of the system was suppressed")
                            if notes is "yes":
                                print(ecmd(r'msg * /time:30 CCS installation is finished. You may restart PC to complete installation.',True))
                        else:
                            print ("Successfully started the Full scan in CCS...")
                            if "7" in os_details:
                                pass
                            else:
                                if scan is "yes":
                                    Triggerfullscan()
                                    print("Reboot of the system wasn't suppressed")
                                    print('System will restart in ' + str(t1) + ' minutes')
                                    print(ecmd(r'shutdown.exe -r -t ' + reboottime + ' /f /c "' + rebootcomment + '"', True))
                    else:
                        print("COMODO Client Security is NOT present")
                        print("Endpoint will NOT reboot, regardless of the SuppressReboot settings")
            else:
                if SuppressReboot is "yes":
                    print("Reboot of the system was suppressed")
                    if notes is "yes":
                        print(ecmd(
                            r'msg * /time:30 Comodo Client Security installation is finished. You may restart PC to complete installation.',
                            True))
                else:
                    print("Reboot of the system was NOT suppressed")
                    print('System will restart in ' + str(t1) + ' minutes')
                    print(ecmd(r'shutdown.exe -r -t ' + reboottime + ' /f /c "' + rebootcomment + '"', True))



else:
    print("Comodo Client Security is installed on the end point")

