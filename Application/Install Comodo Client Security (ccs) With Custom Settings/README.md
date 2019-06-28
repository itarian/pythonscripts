This script is helps you to install Comodo Client Security(ccs) in both Windows and server.

Note:

This script could be used as an auto-remediation procedure for the below custom monitoring script.
https://scripts.comodo.com/frontend/web/topic/check-if-ccs-is-present-in-your-endpoint-if-notinstall-ccs

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
