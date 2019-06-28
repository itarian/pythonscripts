import os
from subprocess import PIPE, Popen
import shutil
import ctypes
import re
try:
    import winreg as _winreg
except ImportError:
    try:
        import _winreg
    except ImportError:
        pass

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
            inst=os.popen("wmic product get name,identifyingnumber").read()
        return inst

def ecmd(command, output=False):
    class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
    with disable_file_system_redirection():
        objt = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
        out, err = objt.communicate()
        ret=objt.returncode
    if not out:
        return ret
    else:
        return '%s\n%s'%(out, err)

def Wrireferify():
	try:
		keyval="SOFTWARE\\COMODO\CIS\\Data"
		reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
		ok = _winreg.OpenKey(reg,keyval,0,_winreg.KEY_WOW64_32KEY | _winreg.KEY_READ)
		val = _winreg.QueryValueEx(ok, "AvDbVersion")[0]
		print(val)
		if val == 0 or val == 1:
			return True
		else:
			return False
	except WindowsError:
		print("key not found")
		return False

if Wrireferify() ==True:
	print( "Antivirus signature database out of date" )
	Source_Path = r'\\ad\Shared'
	EnvTemp = os.environ['ProgramData']
	Dest_Path = os.path.join(EnvTemp, r'Comodo')
	File_Name_CAV = r'bases.cav'
	SP_CAV=os.path.join(Source_Path, File_Name_CAV)
	DP_CAV=os.path.join(Dest_Path, File_Name_CAV)
	
	if not os.path.exists(Dest_Path):
		os.makedirs(Dest_Path)
	if os.path.isdir(Dest_Path):
		print( '"' + Dest_Path + '"' + " folder exists")
	else:
		print( '"' + Dest_Path + '"' + " folder do NOT exists")
	try:
		os.remove(DP_CAV)
	except OSError:
		pass
	try:
		shutil.copy(SP_CAV, DP_CAV)
		command1='"C:\Program Files\COMODO\COMODO Internet Security\cfpconfg.exe" --importAVDB ' + DP_CAV
		command=os.popen(command1).read()
		os.remove(DP_CAV)
		print ('Antivirus signature database was updated Successfully')
	except IOError:
		print ("Unable to copy file. %s" % File_Name_CAV)
else:
	print("Antivirus signature database up to date")
