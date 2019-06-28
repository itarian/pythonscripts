""" Settings """
# Do you want to show warning messages during the installation?
Show_warning_notifications = "yes"
# Do you want to enable MSI Installation log?
Enable_MSI_installation_logging = "yes"
# Please set-up Script_interval_time in seconds the same as repeat time for monitoring (e.g. 5 min = 300, 15 min = 300)
Script_interval_time = 900
# Set time delay before reboot in seconds
Restart_time = 300
""" Settings """



""" Module import section """
print("Importing needed modules")
from subprocess import PIPE, Popen
import re
import ssl
import time
import ctypes
import datetime
import os
import subprocess

try:
    import winreg as _winreg
except ImportError:
    try:
        import _winreg
    except ImportError:
        pass

try:
    import urllib.request as urllib2
except ImportError:
    try:
        import urllib2
    except ImportError:
        pass
print("Needed modules are imported")
""" Module import section """



""" Some of the definitions are used in outer Try-Except clause, that's why they are located below"""

# Check if key is present in the register
def CheckIfKeyIsPresentInTheRegistry(Key_name):
    try:
        reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
        ok = _winreg.OpenKey(reg, Key_name, 0, _winreg.KEY_WOW64_32KEY | _winreg.KEY_READ)
        _winreg.CloseKey(ok)
        print("4.Key is present in registry")
        return True
    except Exception as exception:
        print("5.Exception: " + str(exception))
        return False

# Create 'TimeStampStatus' file and write current time
def WriteTimeStampToTheTimeStampFile():
    print("6.Writing timestamp to the timestamp file: " + str(str('20' + datetime.datetime.now().strftime("%y%m%d%H%M%S"))))
    open(Path_for_time_stamp_file, "w+").write(str('20' + datetime.datetime.now().strftime("%y%m%d%H%M%S")))

# Checking type of the system and settings the right path for TimeStampFile
print("7.Checking type of the system and settings the right path for TimeStampFile:")
Path_for_time_stamp_file = r""
Os_Path = r"C:\Program Files (x86)"
if os.path.exists(Os_Path):
    print("8.OS is 64bit")
    Path_for_time_stamp_file = r"{0}\Program Files (x86)\COMODO\Comodo ITSM\rmmlogs\TimeStampStatus.txt".format(os.environ['systemdrive'])
    print("9.Chosen path: " + Path_for_time_stamp_file)
else:
    print("10.OS is 32bit")
    Path_for_time_stamp_file = r"{0}\Program Files\COMODO\Comodo ITSM\rmmlogs\TimeStampStatus.txt".format(os.environ['systemdrive'])
    print("11.Chosen path: " + Path_for_time_stamp_file)

Path_for_exception_file = r""
Os_Path = r"C:\Program Files (x86)"
if os.path.exists(Os_Path):
    print("12.OS is 64bit")
    Path_for_exception_file = r"{0}\Program Files (x86)\COMODO\Comodo ITSM\rmmlogs\ExceptionStatus.txt".format(os.environ['systemdrive'])
    print("13.Chosen path: " + Path_for_exception_file)
else:
    print("14.OS is 32bit")
    Path_for_exception_file = r"{0}\Program Files\COMODO\Comodo ITSM\rmmlogs\ExceptionStatus.txt".format(os.environ['systemdrive'])
    print("15.Chosen path: " + Path_for_exception_file)
""" Some of the definitions are used in outer Try-Except clause, that's why they are located above"""



""" Outer Try-Except clause section """
try:

    # Path to the downloaded installation file
    Path_to_the_downloaded_CCS_file = os.path.join(os.environ['PROGRAMDATA'], "CCS_Install.msi")
    print("16.Path for the download of the CCS is: " + Path_to_the_downloaded_CCS_file)
    # Get list of the Comodo products
    print("17.Checking installed products...")
    WMI_product_search_result = os.popen('wmic product get name,version, IdentifyingNumber| findstr /i /c:"COMODO Endpoint Security" /c:"COMODO ESM Agent" /c:"COMODO Antivirus for Servers" /c:"COMODO Client - Security"| sort').read()
    print(WMI_product_search_result)

    # Names of the products
    print("18.Setting names for the products")
    ESM = 'COMODO ESM Agent'
    CES = 'COMODO Endpoint Security'
    CCS = 'COMODO Client - Security'
    CAVS = 'COMODO Antivirus for Servers'

    # Version_of_the_CES of the product = "If CES has the name COMODO Client - Security add it version here"
    Version_of_the_CES = '8.3.0.5204'

    # Check type of the system and set the right path for the MSI installation logs
    MSI_logs_switch_for_CCS_install = ""
    MSI_switch_for_uninstall_logs_of_the_ESM = ""
    MSI_switch_for_uninstall_logs_of_the_CES = ""
    MSI_switch_for_uninstall_logs_of_the_CAVS = ""

    if Enable_MSI_installation_logging is "yes":
        print("18.MSI install/uninstall logs are enabled")
        OS_path = r"C:\Program Files (x86)"
        # If OS is 64bit (x86)
        if os.path.exists(OS_path):
            MSI_logs_switch_for_CCS_install = r' /lv*x "C:\Program Files (x86)\COMODO\Comodo ITSM\rmmlogs\CES_Install_MSI ' + str(datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")) + '.log"'
            MSI_switch_for_uninstall_logs_of_the_ESM = r' /lv*x "C:\Program Files (x86)\COMODO\Comodo ITSM\rmmlogs\CESM_Uninstall_MSI ' + str(datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")) + '.log"'
            MSI_switch_for_uninstall_logs_of_the_CES = r' /lv*x "C:\Program Files (x86)\COMODO\Comodo ITSM\rmmlogs\CES_Uninstall_MSI ' + str(datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")) + '.log"'
            MSI_switch_for_uninstall_logs_of_the_CAVS = r' /lv*x "C:\Program Files (x86)\COMODO\Comodo ITSM\rmmlogs\CAVS_Uninstall_MSI ' + str(datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")) + '.log"'
        # If OS is 32bit (x64)
        else:
            MSI_logs_switch_for_CCS_install = r' /lv*x "C:\Program Files\COMODO\Comodo ITSM\rmmlogs\CES_Install_MSI ' + str(datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")) + '.log"'
            MSI_switch_for_uninstall_logs_of_the_ESM = r' /lv*x "C:\Program Files\COMODO\Comodo ITSM\rmmlogs\CESM_Uninstall_MSI ' + str(datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")) + '.log"'
            MSI_switch_for_uninstall_logs_of_the_CES = r' /lv*x "C:\Program Files\COMODO\Comodo ITSM\rmmlogs\CES_Uninstall_MSI ' + str(datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")) + '.log"'
            MSI_switch_for_uninstall_logs_of_the_CAVS = r' /lv*x "C:\Program Files\COMODO\Comodo ITSM\rmmlogs\CAVS_Uninstall_MSI ' + str(datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")) + '.log"'



    """ Class section"""
    print("19.Loading DisableFileSystemRedirection class...")
    class DisableFileSystemRedirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection

        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))

        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
        """Class section"""



    """ Definition section """

    # Run command in CMD
    def DoCommandInCMD(command, output=False):
        print("20.Running next command in the CMD: " + str(command))
        with DisableFileSystemRedirection():
            objt = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
            out, err = objt.communicate()
            ret = objt.returncode
        if not out:
            return ret
        else:
            return '%s\n%s' % (out, err)


    # Check which products are present in the WMI
    def CheckPresenceOfTheComodoProducts():
        print("21. Checking which products are present on the machine via WMI request")
        return DoCommandInCMD('wmic product get name,version,IdentifyingNumber| findstr /i /c:"COMODO Endpoint Security" /c:"COMODO ESM Agent" /c:"COMODO Antivirus for Servers" /c:"COMODO Client - Security"| sort')

    # Check if OS is Microsoft server
    def CheckIfOSIsMicrosoftServer():
        print("22.Checking if OS is Microsoft Server...")

        try:
            reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
            hKey = _winreg.OpenKey(reg, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion")
            value = _winreg.QueryValueEx(hKey, "ProductName")
            if "Server" in value[0]:
                _winreg.CloseKey(hKey)
                print("23. OS is Microsoft server")
                return True
            else:
                _winreg.CloseKey(hKey)
                print("24. OS is not Microsoft server")
                return False
        except Exception as exception:
            print("25. Exception:" + str(exception))
            return False



    """ Uninstall definition section """

    # Uninstall ESM if it is present
    def Uninstall(Product_name, Product_guid, MSI_logs_switch):
        print("26.Starting process of " + Product_name + " uninstallation...")

        # Steps only for ESM Agent
        if Product_name == ESM:
            # Kill ESM processes if they are running
            print("27.Killing ESM processes if the are running...")
            DoCommandInCMD(r'taskkill /f /im AgnService.exe', True)
            DoCommandInCMD(r'taskkill /f /im AgnTray.exe', True)
            print("28.Running ESM MSI uninstall command")
            Result_of_the_uninstall = DoCommandInCMD(r'MsiExec.exe /X ' + Product_guid + ' /q' + MSI_logs_switch, True)
        else:
            # Delete ESM key from registry
            print("29.Checking and deleting ESM key from the registry if it is present")
            if CheckIfKeyIsPresentInTheRegistry('SOFTWARE\COMODO\CIS\ESM'):
                DoCommandInCMD(r'reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\COMODO\CIS\ESM" /f', True)
            # Uninstall CES via MSI service
            print("30.Running MSI uninstall command for the product: " + Product_name)
            Result_of_the_uninstall= DoCommandInCMD(r'MsiExec.exe /X ' + Product_guid + ' /quiet REBOOT=ReallySuppress REMOVE=ALL' + MSI_logs_switch, True)

        # Check if uninstall is successful
        print("31.Checking results of the " + Product_name + " uninstall")
        if Result_of_the_uninstall == 3010 or Result_of_the_uninstall == 0 or Result_of_the_uninstall == 1641:
            print("32." + Product_name + " is uninstalled successfully")
        else:
            print("33.Failed to uninstall " + Product_name + ". Check MSI logs for details")
            print("Result of the uninstall: " + str(Result_of_the_uninstall))
            raise Exception("Failed to uninstall " + Product_name + ". Please check MSI logs for details")
    """ Uninstall definition section """



    # Check type of the OS
    def OSPlatformType():
        true_platform = os.environ['PROCESSOR_ARCHITECTURE']
        try:
            true_platform = os.environ["PROCESSOR_ARCHITEW6432"]
        except KeyError:
            pass
            # true_platform not assigned to if this does not exist
        return true_platform

    # Download install file for CCS
    def DownloadInstallationFileForCCS():
        print("34.Starting download process for CCS .msi")
        # Check system type
        archi = OSPlatformType()
        # If system is 32bit (x86)
        if archi == "x86":
            print("35.OS type is 32 bit")
            Download_URL = "https://download.comodo.com/itsm/CIS_x86.msi"
        # If system is 64bit (x86)
        else:
            print("36.OS type is 64 bit")
            Download_URL = "https://download.comodo.com/itsm/CIS_x64.msi"

        # Try to download files via Python built-in modules
        try:
            print("37.Trying to download files via Python built-in modules...")
            print('38.Downloading required Comodo Client Security installation file to the ' + Path_to_the_downloaded_CCS_file)
            try:
                context = ssl._create_unverified_context()
                f = urllib2.urlopen(Download_URL, context=context)
            except:
                f = urllib2.urlopen(Download_URL)
            # Read all data from the URL
            print("39.Reading data from " + Download_URL)
            data = f.read()
            # Write data to the file
            print("40. Writing data to the file")
            with open(Path_to_the_downloaded_CCS_file, "wb") as code:
                code.write(data)
            # Check if the file was downloaded
            if os.path.isfile(Path_to_the_downloaded_CCS_file):
                print('41.Comodo Client security has been downloaded successfully here ' + Path_to_the_downloaded_CCS_file)
            else:
                print("42.File wasn't downloaded successfully")
                raise Exception("File wasn't downloaded successfully, trying another method...")
        # Another way to download via PowerShell if the first one is failed
        except Exception as exception:
            print(str(exception))
            print("Trying alternative download method")
            subprocess.run("powershell Invoke-WebRequest {} -OutFile {}".format(Download_URL, Path_to_the_downloaded_CCS_file), shell=True)


    # Install CCS
    def InstallCCS():
        print("43.Starting process of CCS installation...")
        archi = OSPlatformType()

        if Show_warning_notifications is "yes":
            DoCommandInCMD(r'msg * /time:30 CCS installation is started. Do not restart PC until next anouncement.', True)

        # If OS is 32bit (x86) install CCS and force ITSM agent connect to the CCS
        if archi == "x86":
            print("44.OS type is 32bit")
            if DoCommandInCMD('msiexec /i  "' + Path_to_the_downloaded_CCS_file + '"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=1 CES_FIREWALL=1 CES_ANTIVIRUS=1 INSTALLFIREWALL=1' + MSI_logs_switch_for_CCS_install, True) == 3010:
                print("45.CCS is installed successfully")
                print("46.Forcing ITSM agent connection...")
                DoCommandInCMD('"C:\Program Files\COMODO\Comodo ITSM\ITSMService.exe" -c 4')
            else:
                print("46.Failed to Install CCS")
                raise Exception("Failed to install CCS. Please check MSI logs for details")

        # If OS is 64bit or server
        else:
            print("47.OS type is 64bit")
            # Check if server
            if CheckIfOSIsMicrosoftServer():
                Command_for_install = 'msiexec /i  "' + Path_to_the_downloaded_CCS_file + '"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=1 CES_FIREWALL=0 CES_ANTIVIRUS=1 AV_FOR_SERVERS=1' + MSI_logs_switch_for_CCS_install
            else:
                Command_for_install = 'msiexec /i  "' + Path_to_the_downloaded_CCS_file + '"  /quiet REBOOT=ReallySuppress CESMCONTEXT=1 MAKE_CESM_DEFAULT_CONFIG=1 CES_SANDBOX=1 CES_FIREWALL=1 CES_ANTIVIRUS=1 INSTALLFIREWALL=1' + MSI_logs_switch_for_CCS_install

            # Check if CCS is installed for server or 64bit machine install CCS and force ITSM agent connect to the CCS
            Result_of_the_install = DoCommandInCMD(Command_for_install, True)
            if Result_of_the_install == 3010:
                print("48.CCS is installed successfully")
                print("49.Forcing ITSM agent connection...")
                DoCommandInCMD('"C:\Program Files (x86)\COMODO\Comodo ITSM\ITSMService.exe" -c 4')
            else:
                print("49.Failed to Install CCS")
                print("50.Result of the install:" + str(Result_of_the_install))
                raise Exception("Failed to install CCS. Please check MSI logs for details")

    def GetGUIDofTheProduct(Product_name):
        print("51.Trying to get guid of the " + Product_name)
        GUID = ""
        if Product_name == ESM:
            GUID = re.findall('{.*}', re.findall('{.*}\s\sCOMODO\sESM\sAgent ', WMI_product_search_result)[0])[0]
            print("Guid of the " + Product_name + " is " + GUID)
        if Product_name == CES:
            GUID = re.findall('{.*}', re.findall('{.*}\s\sCOMODO\sEndpoint\sSecurity ', WMI_product_search_result)[0])[0]
            print("Guid of the " + Product_name + " is " + GUID)
        if Product_name == CCS:
            GUID = re.findall('{.*}', re.findall('{.*}\s\sCOMODO\sClient\s-\sSecurity ', WMI_product_search_result)[0])[0]
            print("Guid of the " + Product_name + " is " + GUID)
        if Product_name == CAVS:
            GUID = re.findall('{.*}', re.findall('{.*}\s\sCOMODO\sAntivirus\sfor\sServers ', WMI_product_search_result)[0])[0]
            print("Guid of the " + Product_name + " is " + GUID)
        return GUID

    def RebootTheMachine(Reboot_delay):
        DoCommandInCMD(r'shutdown.exe -r -t ' + str(Reboot_delay) + ' /f', True)


    def UninstallESMIfPresent():
        # If ESM is present
        if WMI_product_search_result.find(ESM) != -1:
            print(ESM + " is present on the machine, starting uninstall process...")
            Uninstall(ESM, GetGUIDofTheProduct(ESM), MSI_switch_for_uninstall_logs_of_the_ESM)
    """ Definition section """



    """ Logic section """
    print("52.Checking which products are installed and deleting them or installing CCS...")
    # If CES is present
    if WMI_product_search_result.find(CES) != -1:
        print("53.Downloading the needed CCS file before the uninstall of the " + CES)
        DownloadInstallationFileForCCS()
        print(ESM + " is present on the machine, starting uninstall process...")
        # Print notification that process of  CES uninstallation has started
        if Show_warning_notifications is "yes":
            DoCommandInCMD(r'msg * /time:30 CES uninstallation is started. Do not restart PC until next announcement.', True)
        Uninstall(CES, GetGUIDofTheProduct(CES), MSI_switch_for_uninstall_logs_of_the_CES)
        print("54.Creating timestamp file")
        WriteTimeStampToTheTimeStampFile()
        UninstallESMIfPresent()
        print("55.Waiting until the monitoring will be turned off...")
        time.sleep(Script_interval_time)
        print("56.Scheduling reboot")
        if Show_warning_notifications == "yes":
            DoCommandInCMD(r'msg * /time:60 Uninstall of CES is finished. PC will be restarted automatically in ' + str(int(Restart_time/60)) + " min", True)
        RebootTheMachine(Restart_time)
        time.sleep(int(Restart_time - 60))
        if Show_warning_notifications == "yes":
            DoCommandInCMD(r'msg * /time:60 Uninstall of CES is finished. PC will be restarted automatically in 1 min', True)
    # If CCS 8.3.0.5204 is present
    elif (WMI_product_search_result.find(CCS) != -1) and (WMI_product_search_result.find(Version_of_the_CES) != -1):
        print("57.Downloading the needed CCS file before the uninstall of the " + CCS + " with the version " + Version_of_the_CES)
        DownloadInstallationFileForCCS()
        print(CCS + " is present on the machine, starting uninstall process...")
        # Print notification that process of  CCS uninstallation has started
        if Show_warning_notifications is "yes":
            DoCommandInCMD(r'msg * /time:30 CCS uninstallation is started. Do not restart PC until next announcement.', True)
        Uninstall(CCS, GetGUIDofTheProduct(CCS), MSI_switch_for_uninstall_logs_of_the_CES)
        print("58.Creating timestamp file")
        WriteTimeStampToTheTimeStampFile()
        UninstallESMIfPresent()
        print("59.Waiting until the monitoring will be turned off...")
        time.sleep(Script_interval_time)
        print("60.Scheduling reboot")
        if Show_warning_notifications == "yes":
            DoCommandInCMD(r'msg * /time:60 Uninstall of CES is finished. PC will be restarted automatically in ' + str(int(Restart_time/60)) + " min", True)
        RebootTheMachine(Restart_time)
        time.sleep(int(Restart_time - 60))
        if Show_warning_notifications == "yes":
            DoCommandInCMD(r'msg * /time:60 Uninstall of CES is finished. PC will be restarted automatically in 1 min', True)

    # If CAVS is present
    elif WMI_product_search_result.find(CAVS) != -1:
        print("61.Downloading the needed CCS file before the uninstall of the " + CAVS)
        DownloadInstallationFileForCCS()
        print(CAVS + " is present on the machine, starting uninstall process...")
        # Print notification that process of  CAVS uninstallation has started
        if Show_warning_notifications is "yes":
            DoCommandInCMD(r'msg * /time:30 CAVS uninstallation is started. Do not restart PC until next announcement.', True)
        Uninstall(CAVS, GetGUIDofTheProduct(CAVS), MSI_switch_for_uninstall_logs_of_the_CAVS)
        print("62.Creating timestamp file")
        WriteTimeStampToTheTimeStampFile()
        UninstallESMIfPresent()
        print("63.Waiting until the monitoring will be turned off...")
        time.sleep(Script_interval_time)
        print("64.Scheduling reboot")
        if Show_warning_notifications == "yes":
            DoCommandInCMD(r'msg * /time:60 Uninstall of CAVS is finished. PC will be restarted automatically in ' + str(int(Restart_time/60)) + " min", True)
        RebootTheMachine(Restart_time)
        time.sleep(int(Restart_time - 60))
        if Show_warning_notifications == "yes":
            DoCommandInCMD(r'msg * /time:60 Uninstall of CAVS is finished. PC will be restarted automatically in 1 min', True)
    # If CCS is present
    elif WMI_product_search_result.find(CCS) != -1:
        print("65.Latest CCS is already installed")
    # If CCS is not present
    else:
        if not os.path.isfile(Path_to_the_downloaded_CCS_file):
            print("66.Start downloading of the CCS install file")
            DownloadInstallationFileForCCS()
        else:
            print("67.Download file is already present, downloading is not required")
        print("68.Start install of the latest CCS")
        UninstallESMIfPresent()
        InstallCCS()
        print("69.Waiting until ITSM agent connects to CCS...")
        print("70.Time for connection is out")
        print("71.Scheduling reboot")
        if Show_warning_notifications == "yes":
            DoCommandInCMD(r'msg * /time:60 Install of CCS is finished. PC will be restarted automatically in ' + str(int(Restart_time/60)) + " min", True)
        RebootTheMachine(Restart_time)
        time.sleep(int(Restart_time - 60))
        if Show_warning_notifications == "yes":
            DoCommandInCMD(r'msg * /time:60 Install of CCS is finished. PC will be restarted automatically in 1 min', True)
    """ Logic section """

# This section is reached only if some exception was raised during the procedure run.
except Exception as exception:
    print("72.Exception was raised during the procedure run")
    print("73.Removing TimeStampFile to trigger alert")
    if os.path.isfile(Path_for_exception_file):
        if os.path.isfile(Path_for_time_stamp_file):
            print("74.Removing timestamp file")
            os.remove(Path_for_time_stamp_file)
    else:
        print("75.Creating exception file: " + Path_for_exception_file)
        open(Path_for_exception_file, "w+").write(str('20' + datetime.datetime.now().strftime("%y%m%d%H%M%S")))
        if not os.path.isfile(Path_for_time_stamp_file):
            WriteTimeStampToTheTimeStampFile()
    raise Exception(exception)
""" Outer Try-Except clause section """
