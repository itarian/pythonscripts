This procedure removes the registry string keys and then goes into the Window Services of the computer and restarts the Windows Update service.

Edit parameters: handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate",0,_winreg.KEY_ALL_ACCESS)##Please edit with your registry path

 

Run this script as system user