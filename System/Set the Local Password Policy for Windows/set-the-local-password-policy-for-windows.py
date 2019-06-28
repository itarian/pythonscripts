passwordexpire='90' #Provide the day for password expiration
Mimimum_password='8' #Provide the minimum characters for the password

import os
pwd_exp=os.popen('net accounts /maxpwage:'+passwordexpire).read()
print pwd_exp
print 'Password will expire after %s days'%passwordexpire

min_pwd=os.popen('net accounts /minpwlen:'+Mimimum_password).read()
print min_pwd
print 'Minimum Password Characters are %s'%Mimimum_password

complexity=r'''
setlocal EnableDelayedExpansion

SecEdit.exe /export /cfg "%temp%\sec-template.cfg" >nul 2>&1

set names= PasswordComplexity 

set values[PasswordComplexity]=1

for /F "delims== tokens=1,*" %%X in ('type "%temp%\sec-template.cfg"') do (
    call :trim "%%X"
    set cur_name=!result!
    for %%I in (%names%) do (
        if "!cur_name!" equ "%%I" (
            set value== !values[%%I]!       
        )
    )

    if not defined value if "%%Y" neq "" (
        call :trim "%%Y"
        set value== !result!        
    )

    echo !cur_name! !value! >> "%temp%\sec-template2.cfg"
    set value=
)

SecEdit.exe /configure /db secedit.sdb /cfg "%temp%\sec-template2.cfg" >nul 2>&1

del /q "%temp%\sec-template2*.cfg" >nul 2>&1

if exist "%~dp0secedit.sdb" del "%~dp0secedit.sdb" >nul 2>&1

goto :eof

:trim 
set result=%~1

set "f=!result:~0,1!" & set "l=!result:~-1!"

if "!f!" neq " " if "!l!" neq " " goto :eof
if "!f!" equ " " set result=!result:~1!
if "!l!" equ " " set result=!result:~0,-1!

call :trim "!result!"
goto :eof
'''

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
    f.write(complexity)
    
with disable_file_system_redirection():
	process = subprocess.Popen([path],stdout=subprocess.PIPE)
	stdout = process.communicate()[0]
	print "---------------------------"
	print "Password Complexity Achieved.."

if os.path.exists(path):
    try:
	os.remove(path)
    except:
        pass


