IF EXIST "%PROGRAMFILES(X86)%" (GOTO 64BIT) ELSE (GOTO 32BIT)

:64BIT
@echo 64-bit...
IF NOT EXIST "C:\Program Files (x86)\COMODO\cWatchEDRAgent\cwagtsrv.exe" GOTO CDMInstall
IF EXIST "C:\Program Files (x86)\COMODO\cWatchEDRAgent\cwagtsrv.exe" GOTO END

:32BIT
echo 32-bit...
IF NOT EXIST "C:\Program Files\COMODO\cWatchEDRAgent\cwagtsrv.exe" GOTO CDMInstall
IF EXIST "C:\Program Files\COMODO\cWatchEDRAgent\cwagtsrv.exe" GOTO END

:CDMInstall
copy /y \\adserver\sharefolder\EDR\Comodo_EDR_Agent_Installer_1.1.260.8_ZkQl@nEkX.exe c:\Comodo_EDR_Agent_Installer_1.1.260.8_ZkQl@nEkX.exe
start /w c:\Comodo_EDR_Agent_Installer_1.1.260.8_ZkQl@nEkX.exe /quiet
GOTO Finish

:Finish
shutdown -r -t 300
GOTO END

:END
