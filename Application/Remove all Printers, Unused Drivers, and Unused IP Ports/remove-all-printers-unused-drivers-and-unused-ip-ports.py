

BAT=r'''
Cd \
Cd Windows\System32
setLocal EnableDelayedExpansion
CLS
 
:: Determine OS
If exist "c:\Users\Default\NTUSER.DAT" goto Win7
If exist "c:\Documents and Settings\All Users\NTUSER.DAT" goto WinXP
 
:WinXP
cls
Echo Removing all printers
:: Printer deletion
CSCRIPT /nologo %windir%\System32\prnmngr.vbs -x
 
:: Delete TCP/IP port
if exist c:\IPPorts.txt del c:\IPPorts.txt
if exist c:\IPPorts2.txt del c:\IPPorts2.txt
if exist c:\IPPorts3.txt del c:\IPPorts3.txt
cls
 
CSCRIPT /nologo %windir%\System32\prnport.vbs -l > c:\IPPorts.txt
type c:\IPPorts.txt | findstr IP_ > c:\IPPorts2.txt
for /f "tokens=* delims=" %%c in ('type c:\IPPorts2.txt') do (
 set LINE=%%c
 >> c:\IPPorts3.txt echo !LINE:~10!
)
for /f "delims=" %%x in (c:\IPPorts3.txt) do CSCRIPT /nologo %windir%\System32\prnport.vbs -d -r %%x
 
del c:\IPPorts.txt
del c:\IPPorts2.txt
del c:\IPPorts3.txt
 
:: Delete all un-used printer drivers
CSCRIPT /nologo %windir%\System32\prndrvr.vbs -x
 
goto Exit
 
:Win7
cls
Echo Removing all printers
:: Printer deletion
CSCRIPT /nologo %windir%\System32\Printing_Admin_Scripts\en-US\prnmngr.vbs -x
 
:: Delete TCP/IP port
if exist c:\IPPorts.txt del c:\IPPorts.txt
if exist c:\IPPorts2.txt del c:\IPPorts2.txt
if exist c:\IPPorts3.txt del c:\IPPorts3.txt
if exist c:\IPPorts4.txt del c:\IPPorts4.txt
cls
 
CSCRIPT /nologo %windir%\System32\Printing_Admin_Scripts\en-US\prnport.vbs -l > c:\IPPorts.txt
type c:\IPPorts.txt | findstr 172.20 > c:\IPPorts2.txt
type c:\IPPorts2.txt | findstr Port > c:\IPPorts3.txt
for /f "tokens=* delims=" %%c in ('type c:\IPPorts3.txt') do (
 set LINE=%%c
 >> c:\IPPorts4.txt echo !LINE:~10!
)
for /f "delims=" %%x in (c:\IPPorts4.txt) do CSCRIPT /nologo %windir%\System32\Printing_Admin_Scripts\en-US\prnport.vbs -d -r %%x
 
del c:\IPPorts.txt
del c:\IPPorts2.txt
del c:\IPPorts3.txt
del c:\IPPorts4.txt
 
:: Delete all used printer drivers
CSCRIPT /nologo %windir%\System32\Printing_Admin_Scripts\en-US\prndrvr.vbs -x
 
goto Exit
 
:Exit
'''
import os
import sys
import platform
import subprocess
import ctypes

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

path=os.environ['programdata']+"\Sample.bat"
with open(path,"w") as f:
    f.write(BAT)
    
with disable_file_system_redirection():
	process = subprocess.Popen([path],stdout=subprocess.PIPE)
	stdout = process.communicate()[0]
	print "execution sucess"
	print stdout

if os.path.exists(path):
	try:
		os.remove(path)
	except:
		pass
